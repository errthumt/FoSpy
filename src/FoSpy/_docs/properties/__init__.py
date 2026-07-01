import re
from pathlib import Path
import json
import os
from warnings import warn


TAB_WIDTH = 80
PROP_URL = "https://errthumt.github.io/FoSpy/latest/expected/"


module_dir = Path(os.path.abspath(__file__)).parent
TEMPLATE_DIR = module_dir / "summary_stubs"
PROP_DESCS = module_dir / "descriptions.json"
PREAMBLE = module_dir / "preamble.md"

CLI_TBL_FMT = "grid"

def table_dict_to_lines(table_dict, mode="cli"):
    from tabulate import tabulate
    tab_kwargs = {
        "headers": "keys",
        "tablefmt": "pipe",
        "maxcolwidths": None
    }
    if mode == "cli":
        first_col = next(iter(table_dict.keys()))
        prop_width = max([len(k) for k in [first_col, *table_dict[first_col]]])

        cols = len(table_dict.keys())
        col_widths = [(TAB_WIDTH - cols - 1 - prop_width) // (cols - 1) for _ in range(cols-1)]

        tab_kwargs["maxcolwidths"] = (prop_width, *col_widths)
        tab_kwargs["tablefmt"] = CLI_TBL_FMT

    txt = tabulate(table_dict, **tab_kwargs)
    lines = txt.splitlines(keepends=True)

    return lines

def _load_all_validators():
    """Dynamically imports all modules in the validators package to trigger decorators."""
    import pkgutil
    import importlib
    from ...parsing import validators
    for _, module_name, _ in pkgutil.walk_packages(validators.__path__, validators.__name__ + "."):
        importlib.import_module(module_name)


val_rules = {
    str: "Any text entry",
    float: "Any decimal number (positive or negative)",
    int: "Any integer (positive or negative)"
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

def build_tables(cls, descs, force_rules=False, mode="cli", urls={}, crossrefs={}):
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

            if mode == "cli":
                desc, urls, crossrefs = _strip_links(desc, urls=urls, crossrefs=crossrefs)

            val_rule = val_rules.get(val, None)
            if val_rule is None:
                if force_rules:
                    raise ValueError(f"No validation rules found for {val}")
                val_rule = "No Rules Found"
            else:
                val_rule = _val_rules_to_txt(val_rule, mode=mode)
                if mode == "cli":
                    val_rule, urls, crossrefs = _strip_links(val_rule, urls=urls, crossrefs=crossrefs)
                # val_rule = val_rule.replace("\n- ", "</li><li>").replace("- ", "<li>") + "</li>"
                # val_rule = val_rule.replace("\n", "<br>")
                # val_rule = f"<ul>{val_rule}</ul>"
            out[key]["Property"].append(prop)
            out[key]["Description"].append(desc)
            out[key]["Validation Rules"].append(val_rule)

    return out, urls, crossrefs

def find_desc(cls, prop, descs):
    for parent in cls.__mro__:
        cls_nm = parent.__name__
        prop_set = descs.get(cls_nm, {})
        if prop in prop_set:
            desc = prop_set[prop]["desc"]
            return desc
    raise KeyError(f"Could not find description for {cls.__name__}.{prop}")

def _wrap_url_clickable(url, max_len=25):
    """
    Splits a URL into multiple lines matching max_len.
    Wraps each chunk in an OSC 8 sequence pointing to the FULL URL.
    """
    if not url:
        return ""
        
    chunks = []
    # Split the URL into text segments of max_len width
    for i in range(0, len(url), max_len):
        chunk_text = url[i:i + max_len]
        
        # Wrap the visual chunk in an OSC 8 sequence pointing to the full URL
        clickable_chunk = f"\033]8;;{url}\033\\{chunk_text}\033]8;;\033\\"
        chunks.append(clickable_chunk)
        
    # Join with newlines so tabulate stacks them vertically within the cell
    return " \n ".join(chunks)


def _get_block_module_path(attr_name: str) -> str:
    """Gets the actual module path for a specific attribute in FoSpy.blocks."""
    import inspect
    import FoSpy.blocks

    # 1. Retrieve the attribute safely from the parent module
    try:
        obj = getattr(FoSpy.blocks, attr_name)
    except AttributeError:
        raise AttributeError(f"'{attr_name}' does not exist in FoSpy.blocks")
        
    # 2. Extract the true source module name
    # inspect.getmodule() works reliably for classes, functions, and methods
    module_obj = inspect.getmodule(obj)
    
    if module_obj is not None:
        return module_obj.__name__
        
    # Fallback for basic data types (ints, strings) that lack module metadata
    if hasattr(obj, '__module__'):
        return obj.__module__
        
    return FoSpy.blocks.__name__


def _strip_links(txt, urls=None, crossrefs=None):
    txt = txt.replace("`","")

    urls = urls or {}
    crossrefs = crossrefs or {}

    urls.setdefault("_repeats_", {})
    url_rpts = urls["_repeats_"]

    crossrefs.setdefault("_repeats_", {})
    cr_rpts = crossrefs["_repeats_"]

    # Pattern matches either:
    # 1. (?P<cr_text>\[.*?\])(?P<cr_link>\[.*?\]) -> [crossref text][crossref]
    # 2. (?P<url_text>\[.*?\])(?P<url_link>\(.*?\)) -> [url text](url)
    # Note: We escape the outer brackets/parentheses to match literal syntax
    pattern = r'(?P<cr_text>\[[^\]]+\])(?P<cr_link>\[[^\]]+\])|(?P<url_text>\[[^\]]+\])\((?P<url_link>[^\)]+)\)'

    def replacer(match):
        # --- Crossref Branch ---
        if match.group('cr_text'):
            # Strip the outer brackets from the match groups
            text = match.group('cr_text')[1:-1]
            link = match.group('cr_link')[1:-1]

            if link.startswith("blockdocs-"):
                block_nm = link[10:]
                link = _get_block_module_path(block_nm)
            
            # Handle repeats
            rpts = cr_rpts
            if text in rpts:
                if link not in rpts[text]:
                    idx = len(rpts[text])
                    rpts[text].append(link)
                else:
                    idx = rpts[text].index(link)

                unique_text = f"{text} ({idx})" if idx > 0 else text
            else:
                rpts[text] = [link]
                unique_text = text
            
            crossrefs[unique_text] = link
                
            replace = f"<{unique_text}>"
            return replace

        # --- URL Branch ---
        elif match.group('url_text'):
            # Strip outer brackets and parentheses
            text = match.group('url_text')[1:-1]
            link = match.group('url_link')
            
            if link.startswith("#"):
                link = PROP_URL + link

            # Handle repeats
            rpts = url_rpts
            if text in rpts:
                if link not in rpts[text]:
                    idx = len(rpts[text])
                    rpts[text].append(link)
                else:
                    idx = rpts[text].index(link)

                unique_text = f"{text} ({idx})" if idx > 0 else text
            else:
                rpts[text] = [link]
                unique_text = text


            urls[unique_text] = link
                
            replace = f"~{unique_text}~"
            return replace

        return match.group(0) # Fallback (shouldn't be reached)

    # Execute the single-scan replacement
    modified_txt = re.sub(pattern, replacer, txt)

    return modified_txt, urls, crossrefs

def _get_header_lines(cls_nm, parent_nm, mode="cli"):
    if mode in ("md-tb", "md"):

        return [
            f"\n### `{cls_nm}`\n\n",
            f"[Class Documentation][blockdocs-{cls_nm}]\n\n",
            f"**[Subclass of `{parent_nm}`](#{parent_nm.lower()})**\n\n",
        ]
    else:
        if mode != "cli":
            warn(f"Unrecognized mode: {mode}. Defaulting to CLI formatting for header lines.")
        return [
            f"===== Property Summary for {cls_nm} =====\n",
            "URLs are surrounded by ~ characters. FoSpy cross-references "
            "are surrounded by <> characters.\n",
            "URL and cross-reference destinations are listed at the end of this message.\n\n",
            f"~Subclass of {parent_nm}~\n\n"
        ]

def _md_to_mode(txt, mode="cli", urls={}, crossrefs={}):
    if mode in ("md", "md-tb"):
        return txt
    
    from tabulate import tabulate

    urls = urls.copy()
    crossrefs = crossrefs.copy()
    indent = 0
    out_txt = ""
    current_h = 1
    lines = txt.splitlines(keepends=True)

    for ln in lines:
        ln, urls, crossrefs = _strip_links(ln, urls=urls, crossrefs=crossrefs)
        ln = ln.replace("`", "")

        if ln.startswith("#"):
            h = ln.count("#")
            if h > current_h:
                indent += 1
            elif h < current_h:
                indent -= 1
            current_h = h

            header = ln.lstrip("#").strip()
            header = f"==== {header} ====\n"
            out_txt += "  "*indent + header + "\n"
        else:
            out_txt += "  "*indent + ln

    urls.pop("_repeats_", None)
    if urls != {}:
        out_txt += "\n\n==== URLS ====\n\n"

        key_width = max([len(k) for k in ["Text Reference", *urls.keys()]])
        url_width = TAB_WIDTH - key_width - 3

        urls = {
            k: _wrap_url_clickable(v, max_len=url_width)
            for k, v in urls.items()
        }
        out_txt += tabulate(urls.items(), headers=["Text Reference", "URL"],
                            tablefmt=CLI_TBL_FMT, maxcolwidths=(key_width, None))

    crossrefs.pop("_repeats_", None)
    if crossrefs != {}:
        out_txt += "\n\n==== CROSS-REFERENCES ====\n\n"

        key_width = max([len(k) for k in ["Text Reference", *crossrefs.keys()]])
        ref_width = TAB_WIDTH - key_width - 3

        out_txt += tabulate(crossrefs.items(), headers=["Text Reference", "Reference"],
                            tablefmt=CLI_TBL_FMT, maxcolwidths=(key_width, ref_width))
        

    return out_txt



def get_summary(cls, force_rules=False, mode="cli"):
    cls_nm = cls.__name__
    parent_nm = cls.__bases__[0].__name__

    descs = get_descs()
    temp_dir = TEMPLATE_DIR

    urls = {
        "Full Fospy Property Documentation": PROP_URL,
        f"Subclass of {parent_nm}": f"{PROP_URL}#{parent_nm.lower()}"
    }
    crossrefs = {}

    tables, urls, crossrefs = build_tables(cls, descs, force_rules=force_rules, mode=mode, urls=urls, crossrefs=crossrefs)
    req_tb_lines = table_dict_to_lines(tables["req"], mode=mode)
    opt_tb_lines = table_dict_to_lines(tables["opt"], mode=mode)

    stub_path = temp_dir / f"{cls_nm}.md"

    full_summary = _get_header_lines(cls_nm, parent_nm, mode=mode)

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
        full_summary.append("\n\n")

    if not (opt_hd_found and
            any(col==[] for col in tables["opt"].values())):
        full_summary.append("#### Optional properties\n\n")
        full_summary.extend(opt_tb_lines)
        full_summary.append("\n\n")

    full_summary.extend(temp_lines)

    txt = "".join(full_summary)



    txt = _md_to_mode(txt, mode=mode, urls=urls, crossrefs=crossrefs)
    return txt

def get_descs():
    with open(PROP_DESCS, "r", encoding="utf-8") as f:
        descs = json.load(f)
    return descs

def get_prop_md():
    from ... import blocks as blk_module

    block_lst = sorted(blk_module.__all__)

    txt = "\n## Expected Property Tables\n"


    for cls_nm in block_lst:
        cls = getattr(blk_module, cls_nm)

        if isinstance(cls, type) and issubclass(cls, blk_module.SingleBlock):
            txt += get_summary(cls, mode="md-tb")
            txt += "---\n"

    return txt

def write_prop_md(md_path):
    with open(PREAMBLE, "r", encoding="utf-8") as f:
        preamble = f.read()

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(preamble + get_prop_md())


def _validator_rules(*args):
    from ..._docs.properties import val_rules
    def decorator(func, a=args):
        val_rules[func] = a
        return func
    return decorator

def _val_rules_to_txt(rules, mode="cli", indent=0):
    txt = ""
    if not isinstance(rules, (list, tuple)):
        rules = [rules]
    for i,rule in enumerate(rules):
        if isinstance(rule, (list, tuple)):
            i_txt = _val_rules_to_txt(rule, mode=mode, indent=indent+1)
        elif isinstance(rule, str):
            i_txt = rule
        else:
            raise ValueError(f"Unrecognized structure for validation rules: {rule}")

        if mode == "md-tb":
            if i == 0:
                txt += "<ul>"
            
            txt += f"<li>{i_txt}</li>"

            if i == len(rules)-1:
                txt += "</ul>"
        else:
            if mode not in ("cli", "md"):
                warn(f"Unrecognized mode: {mode}. Defaulting to markdown/CLI formatting for list.")
            txt += f"{' '*indent}- {i_txt}\n"
    return txt
    



