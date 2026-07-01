from scripts._utils import set_sandbox_cwd
from pathlib import Path
import json

import FoSpy
block_lst = sorted(FoSpy.blocks.__all__)

def table_dict_to_lines(table_dict):
    lines = ["| " + " | ".join(table_dict.keys()) + " |\n",
             "| " + " | ".join(["-"*len(k) for k in table_dict.keys()]) + " |\n"]

    for cells in zip(*table_dict.values()):
        line = "| " + " | ".join(cells) + " |\n"
        lines.append(line)
    lines.append("\n")

    return lines


def build_tables(cls, descs, val_rules={}):
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
            val_rule = val_rules.get(val, "Rules not found")
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

TABLES = Path("exp_tables.md")
DESCS = Path("exp_descs.json")
MD_OUT = Path("expected.md")
PREAMBLE = Path("exp_pre.md")
STUBS = Path("stubs")


def get_stub(temp_dir, cls, descs, val_rules={}):
    cls_nm = cls.__name__
    parent_nm = cls.__bases__[0].__name__

    tables = build_tables(cls, descs, val_rules)
    req_tb_lines = table_dict_to_lines(tables["req"])
    opt_tb_lines = table_dict_to_lines(tables["opt"])

    stub_path = temp_dir / f"{cls_nm}.md"

    full_stub = [
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
        full_stub.append("#### Required properties\n\n")
        full_stub.extend(req_tb_lines)

    if not (opt_hd_found and
            any(col==[] for col in tables["opt"].values())):
        full_stub.append("#### Optional properties\n\n")
        full_stub.extend(opt_tb_lines)

    full_stub.extend(temp_lines)

    return "".join(full_stub)

def get_tables():
    with open(DESCS, "r", encoding="utf-8") as f:
        descs = json.load(f)

    txt = "\n## Expected Property Tables\n"


    for cls_nm in block_lst:
        cls = getattr(FoSpy.blocks, cls_nm)

        if isinstance(cls, type) and issubclass(cls, FoSpy.blocks.SingleBlock):
            txt += get_stub(STUBS, cls, descs)

    return txt

def build_md():
    with open(PREAMBLE, "r", encoding="utf-8") as f:
        preamble = f.read()

    with open(MD_OUT, "w", encoding="utf-8") as f:
        f.write(preamble + get_tables())


if __name__ == "__main__":
    set_sandbox_cwd()
    #main()
    build_md()

