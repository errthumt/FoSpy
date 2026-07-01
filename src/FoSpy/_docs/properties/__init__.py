from pathlib import Path
import json
import os




module_dir = Path(os.path.abspath(__file__)).parent
STUBS_DIR = module_dir / "summary_stubs"
PROP_DESCS = module_dir / "descriptions.json"
PREAMBLE = module_dir / "preamble.md"



def table_dict_to_lines(table_dict):
    lines = ["| " + " | ".join(table_dict.keys()) + " |\n",
             "| " + " | ".join(["-"*len(k) for k in table_dict.keys()]) + " |\n"]

    for cells in zip(*table_dict.values()):
        line = "| " + " | ".join(cells) + " |\n"
        lines.append(line)
    lines.append("\n")

    return lines

def _load_all_validators():
    """Dynamically imports all modules in the validators package to trigger decorators."""
    import pkgutil
    import importlib
    from ...parsing import validators
    for _, module_name, _ in pkgutil.walk_packages(validators.__path__, validators.__name__ + "."):
        importlib.import_module(module_name)


val_rules = {
    str: "- Any text entry",
    float: "- Any decimal number (positive or negative)",
    int: "- Any integer (positive or negative)"
}
"""
Summaries of validation rules mapped to validator functions.

Rule lists are formatted as markdown lists before being mapped to a validator.

Possible Validators:
    `SingleBlock` subclasses:
        A single rule points to the validating class.
    `ListBlock` subclasses:
        A single rule points to the `SingleBlock` class enforced by the `ListBlock`.
    Other Validators:
        The validator function is decorated with `@_validator_rules()`, which specifies a list of rules to be mapped in this dictionary.
"""

def build_tables(cls, descs, force_rules=False):
    _load_all_validators()
    def empty_gen():
        while True:
            mt = {"Property": [], "Description": [], "Validation Rules": []}
            yield mt

    empty = empty_gen()

    out = {"req": next(empty), "opt": next(empty)}

    required = cls.build_req_validators()

    optional = cls.build_validators()

    for (key, val_set) in (("req",required), ("opt",optional)):
        for prop, val in val_set.items():
            if prop == "ext":
                continue
            if key == "req":
                optional.pop(prop, None)
            desc = find_desc(cls, prop, descs)
            val_rule = val_rules.get(val, None)
            if val_rule is None:
                if force_rules:
                    raise ValueError(f"No validation rules found for {val}")
                val_rule = "No Rules Found"
            else:
                val_rule = val_rule.replace("\n- ", "</li><li>").replace("- ", "<li>") + "</li>"
                val_rule = val_rule.replace("\n", "<br>")
                val_rule = f"<ul>{val_rule}</ul>"
            out[key]["Property"].append(prop)
            out[key]["Description"].append(desc)
            out[key]["Validation Rules"].append(val_rule)

    return out

def find_desc(cls, prop, descs):
    for parent in cls.__mro__:
        cls_nm = parent.__name__
        prop_set = descs.get(cls_nm, {})
        if prop in prop_set:
            desc = prop_set[prop]["desc"]
            return desc
    raise KeyError(f"Could not find description for {cls.__name__}.{prop}")



def get_summary(temp_dir, cls, descs, force_rules=False):
    cls_nm = cls.__name__
    parent_nm = cls.__bases__[0].__name__

    tables = build_tables(cls, descs, force_rules=force_rules)
    req_tb_lines = table_dict_to_lines(tables["req"])
    opt_tb_lines = table_dict_to_lines(tables["opt"])

    stub_path = temp_dir / f"{cls_nm}.md"

    full_summary = [
        f"\n### `{cls_nm}`\n\n",
        f"[Class Documentation][blockdocs-{cls_nm}]\n\n",
        f"**[Subclass of `{parent_nm}`](#{parent_nm.lower()})**\n\n",
    ]

    temp_lines = []

    if stub_path.exists():
        with open(stub_path, "r", encoding="utf-8") as f:
            template_lines = f.readlines()
    else:
        template_lines = []

    req_hd_found = False
    req_tb_found = False

    opt_hd_found = False
    opt_tb_found = False

    for line in template_lines:
        stripped = line.strip()

        if (line.startswith("#") and
            not (
                req_hd_found == req_tb_found and
                opt_hd_found == opt_tb_found
            )):
            raise Exception("Property table headers must be accompanied by a table placeholder")

        if stripped.endswith("# Required properties"):
            if req_hd_found:
                Exception("Duplicate required properties header")
            req_hd_found = True

        if stripped.endswith("# Optional properties"):
            if opt_hd_found:
                raise Exception("Duplicate optional properties header")
            opt_hd_found = True

        if stripped == "<prop_table>":
            if opt_hd_found:
                opt_tb_found = True
                temp_lines.extend(req_tb_lines)
            elif req_hd_found:
                req_tb_found = True
                temp_lines.extend(opt_tb_lines)
            else:
                raise Exception("Property table placeholder found without preceding header")

            continue

        temp_lines.append(line)

    if not (req_hd_found and
            any(col==[] for col in tables["req"].values())):
        full_summary.append("#### Required properties\n\n")
        full_summary.extend(req_tb_lines)

    if not (opt_hd_found and
            any(col==[] for col in tables["opt"].values())):
        full_summary.append("#### Optional properties\n\n")
        full_summary.extend(opt_tb_lines)

    full_summary.extend(temp_lines)

    return "".join(full_summary)

def get_all_props():
    from ... import blocks as blk_module

    block_lst = sorted(blk_module.__all__)

    with open(PROP_DESCS, "r", encoding="utf-8") as f:
        descs = json.load(f)

    txt = "\n## Expected Property Tables\n"


    for cls_nm in block_lst:
        cls = getattr(blk_module, cls_nm)

        if isinstance(cls, type) and issubclass(cls, blk_module.SingleBlock):
            txt += get_summary(STUBS_DIR, cls, descs)
            txt += "---\n"

    return txt

def write_prop_md(md_path):
    with open(PREAMBLE, "r", encoding="utf-8") as f:
        preamble = f.read()

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(preamble + get_all_props())


def _validator_rules(*args):
    from ..._docs.properties import val_rules
    lst = ["- " + arg for arg in args]
    txt = "\n".join(lst)
    def decorator(func, txt=txt):
        val_rules[func] = txt
        return func
    return decorator

