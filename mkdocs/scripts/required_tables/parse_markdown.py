from pathlib import Path
from markdown_it import MarkdownIt
from mdformat.renderer import MDRenderer
import mdformat

import pkgutil
import importlib
import inspect
import FoSpy  # your package root


MD_PATH = Path("mkdocs/docs/expected/index.md")
#OUT_PATH = Path("mkdocs/scripts/required_tables/index_with_links.md")
OUT_PATH = MD_PATH
TEMPLATE_PATH = Path("mkdocs/scripts/required_tables/class_template.md")

def find_class_module_path(class_name: str) -> str | None:
    """
    Search the FoSpy package for a class with the given name.
    Return its fully-qualified module path:
        FoSpy.blocks.<submodule>.<ClassName>
    """
    root = FoSpy.__path__  # namespace for pkgutil.walk_packages

    for module_info in pkgutil.walk_packages(root, FoSpy.__name__ + "."):
        module_name = module_info.name

        try:
            module = importlib.import_module(module_name)
        except Exception:
            continue  # skip modules that fail to import

        # Walk attributes in the module
        for attr_name in dir(module):
            if attr_name != class_name:
                continue

            obj = getattr(module, attr_name)
            if inspect.isclass(obj) and obj.__name__ == class_name:
                return f"{obj.__module__}.{obj.__name__}"

    return None



def parse_markdown(md_text: str, tables=False):
    """Parse markdown into markdown-it-py tokens."""
    if tables:
        md = MarkdownIt("gfm-like").enable("table")
    else:
        md = MarkdownIt("commonmark")
    return md.parse(md_text)

def get_template_tokens():
    """Load the class documentation template and parse it into tokens."""
    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    return parse_markdown(template_text)

def get_paragraph_tokens(para_text, tok):
    para_open = tok.__class__(
        type="paragraph_open",
        tag="p",
        nesting=1,
        attrs={},
        map=[None, None],   # markdown-it often uses [line, line+1], but None is safe
        level=tok.level,
        children=None,
        content="",
        markup="",
        info="",
        meta={},
        block=True,
        hidden=False,
    )

    # inline with proper children
    inline_token = tok.__class__(
        type="inline",
        tag="",
        nesting=0,
        attrs={},
        map=[None, None],
        level=tok.level + 1,
        children=[
            tok.__class__(
                type="text",
                tag="",
                nesting=0,
                attrs={},
                map=None,
                level=0,
                children=None,
                content=para_text,
                markup="",
                info="",
                meta={},
                block=False,
                hidden=False,
            )
        ],
        content=para_text,
        markup="",
        info="",
        meta={},
        block=True,
        hidden=False,
    )

    # paragraph_close
    para_close = tok.__class__(
        type="paragraph_close",
        tag="p",
        nesting=-1,
        attrs={},
        map=None,
        level=tok.level,
        children=None,
        content="",
        markup="",
        info="",
        meta={},
        block=True,
        hidden=False,
    )
    return para_open, inline_token, para_close

def pop_before(strings, comparison):
    """
    Remove and return all strings alphabetically before `comparison`.
    Mutates `strings` in place and returns (removed, remaining).
    """
    removed = [s for s in strings if s < comparison]
    remaining = [s for s in strings if s >= comparison]
    strings[:] = remaining
    return removed, strings


def get_heading_tokens(heading_text, tok):
    """
    Create a new H2 heading token triplet matching markdown-it-py's structure:
        heading_open
        inline (with code_inline child)
        heading_close

    heading_text should be something like "`ClassName`".
    """
    # Extract the class name without backticks
    class_name = heading_text.strip("`")

    # --- heading_open ---
    heading_open = tok.__class__(
        type="heading_open",
        tag="h2",
        nesting=1,
        attrs={},
        map=[None, None],     # safe default
        level=tok.level,      # same level as the original heading
        children=None,
        content="",
        markup="##",
        info="",
        meta={},
        block=True,
        hidden=False,
    )

    # --- inline token with code_inline child ---
    code_child = tok.__class__(
        type="code_inline",
        tag="code",
        nesting=0,
        attrs={},
        map=None,
        level=0,
        children=None,
        content=class_name,
        markup="`",
        info="",
        meta={},
        block=False,
        hidden=False,
    )

    heading_inline = tok.__class__(
        type="inline",
        tag="",
        nesting=0,
        attrs={},
        map=[None, None],
        level=tok.level + 1,
        children=[code_child],
        content=heading_text,   # e.g. "`Treatment`"
        markup="",
        info="",
        meta={},
        block=True,
        hidden=False,
    )

    # --- heading_close ---
    heading_close = tok.__class__(
        type="heading_close",
        tag="h2",
        nesting=-1,
        attrs={},
        map=None,
        level=tok.level,
        children=None,
        content="",
        markup="##",
        info="",
        meta={},
        block=True,
        hidden=False,
    )

    return heading_open, heading_inline, heading_close


def add_class_doc_links(tokens, diffs={}):
    """
    Insert a `[Class Documentation][FoSpy.blocks.<ClassName>]`
    link immediately after each class heading of the form:

        ## `ClassName`
    """
    missing_classes = diffs.get("missing_classes", [])
    missing_required = diffs.get("missing_required", {})
    missing_optional = diffs.get("missing_optional", {})

    new_tokens = []
    i = 0
    tables_start = False
    template_tokens = get_template_tokens()
    while i < len(tokens):
        tok = tokens[i]
        if tok.type == "heading_open" and tok.tag == "h1":
            inline = tokens[i + 1]
            if inline.type == "inline" and "Expected Property Tables" in inline.content:
                tables_start = True
                i+=1
                new_tokens.append(tok)
                continue
        elif not tables_start:
            i+=1
            new_tokens.append(tok)
            continue

        elif tok.type == "paragraph_open" and tokens[i+1].content.startswith("!table_check"):
            # Skip the next 3 tokens (paragraph_open, inline, paragraph_close)
            i += 3
            continue

        # Detect class header: ## `ClassName`
        if tok.type == "heading_open" and tok.tag == "h2":
            inline = tokens[i + 1]

            # --- FIX FOR COMMONMARK ---
            # Extract class name from inline children
            class_name = None
            if inline.children:
                for child in inline.children:
                    if child.type == "code_inline":
                        class_name = child.content
                        break

            # Fallback: use inline.content (rarely needed)
            if class_name is None:
                class_name = inline.content.strip("`")

            new_headings, missing_classes = pop_before(missing_classes, class_name)
            for heading in new_headings:
                pre_text = "!table_check:Placeholder for missing class."
                req_text = f"!table_check: Missing required properties: {missing_required.get(heading, [])}"
                opt_text = f"!table_check: Missing optional properties: {missing_optional.get(heading, [])}"
                new_tokens.extend([*get_heading_tokens(f"`{heading}`", tok), 
                                   *get_paragraph_tokens(pre_text, tok),
                                   *get_paragraph_tokens(req_text, tok),
                                   *get_paragraph_tokens(opt_text, tok),
                                   *template_tokens])
            
            new_tokens.append(tok)
            if "Class Documentation" not in tokens[i+4].content:
                # Build the link text
                link_text = f"[Class Documentation][{find_class_module_path(class_name) or 'UnknownClass'}]"

                
                # Insert a paragraph_open, inline, paragraph_close sequence
                new_tokens.extend([
                    tokens[i+1],
                    tokens[i+2],
                    *get_paragraph_tokens(link_text, tok)
                ])
                i += 2

            missing_req = missing_required.get(class_name, [])
            missing_opt = missing_optional.get(class_name, [])
            if missing_req:
                new_tokens.extend(get_paragraph_tokens(f"!table_check: Missing required properties: {missing_req}", tok))
            if missing_opt:
                new_tokens.extend(get_paragraph_tokens(f"Missing optional properties: {missing_opt}", tok))
        else:
            new_tokens.append(tok)
        i += 1

    return new_tokens

def extract_property_tables(tokens):
    """
    Extract class → {required: [...], optional: [...]} from markdown tokens.
    """
    current_class = None
    current_section = None
    tables = {}
    tables_start = False
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok.type == "heading_open" and tok.tag == "h1":
            inline = tokens[i + 1]
            if inline.type == "inline" and "Expected Property Tables" in inline.content:
                tables_start = True
                i+=1
                continue
        elif not tables_start:
            i+=1
            continue

        # Detect class header: ## `Annealing`
        if tok.type == "heading_open" and tok.tag == "h2":
            inline = tokens[i + 1]
            text = inline.content.strip("`")
            current_class = text
            tables.setdefault(current_class, {})
            i += 2
            continue

        # Detect Required / Optional section headers
        if tok.type == "heading_open" and tok.tag == "h3":
            inline = tokens[i + 1]
            text = inline.content.lower()
            if "required" in text:
                current_section = "required"
            elif "optional" in text:
                current_section = "optional"
            i += 2
            continue

        # Detect table
        if tok.type == "table_open":
            props = []
            j = i + 1

            # Collect all table cell contents
            while tokens[j].type != "table_close":
                if tokens[j].type == "td_open":
                    cell = tokens[j + 1].content.strip()
                    props.append(cell)
                j += 1

            # First column of each row = property name
            # Skip header row (3 columns)
            property_names = props[::3]

            tables[current_class][current_section] = property_names
            i = j + 1
            continue

        i += 1

    return tables

def process_markdown(md_path: Path, diffs={}):
    """Load markdown file, modify tokens, and return new markdown."""
    md_text = md_path.read_text(encoding="utf-8")
    tokens = parse_markdown(md_text)

    # Add class documentation links
    modified_tokens = add_class_doc_links(tokens, diffs=diffs)

    renderer = MDRenderer()
    md_text = renderer.render(modified_tokens,{},{})

    # Convert tokens back to markdown
    new_markdown = mdformat.text(md_text) 
    return new_markdown

from FoSpy.parsing.validation import required_keys, optional_keys


from FoSpy.parsing.validation import required_keys, optional_keys


def diff_property_tables(extracted_tables):
    """
    Compare extracted Markdown tables against FoSpy.parsing.validation
    required_keys and optional_keys.

    Returns a structured diff:
    {
        "missing_classes": [...],
        "extra_classes": [...],
        "missing_required": {class: [...]},
        "missing_optional": {class: [...]},
        "extra_required": {class: [...]},
        "extra_optional": {class: [...]},
    }
    """

    # Convert validation dicts to: class_name -> set(property_names)
    required_map = {
        cls.__name__: set(props.keys())
        for cls, props in required_keys.items()
    }

    optional_map = {
        cls.__name__: set(props.keys())
        for cls, props in optional_keys.items()
    }

    validation_classes = set(required_map.keys()) | set(optional_map.keys())
    md_classes = set(extracted_tables.keys())

    diff = {
        "missing_classes": sorted(validation_classes - md_classes),
        "extra_classes": sorted(md_classes - validation_classes),
        "missing_required": {},
        "missing_optional": {},
        "extra_required": {},
        "extra_optional": {},
    }

    # --- 1. Classes present in BOTH ---
    for cls in md_classes & validation_classes:
        md_required = set(extracted_tables[cls].get("required", []))
        md_optional = set(extracted_tables[cls].get("optional", []))

        val_required = required_map.get(cls, set())
        val_optional = optional_map.get(cls, set())

        # Missing required
        missing_req = sorted(val_required - md_required)
        if missing_req:
            diff["missing_required"][cls] = missing_req

        # Missing optional
        missing_opt = sorted(val_optional - md_optional)
        if missing_opt:
            diff["missing_optional"][cls] = missing_opt

        # Extra required
        extra_req = sorted(md_required - val_required)
        if extra_req:
            diff["extra_required"][cls] = extra_req

        # Extra optional
        extra_opt = sorted(md_optional - val_optional)
        if extra_opt:
            diff["extra_optional"][cls] = extra_opt

    # --- 2. Classes missing from Markdown entirely ---
    for cls in validation_classes - md_classes:
        val_required = required_map.get(cls, set())
        val_optional = optional_map.get(cls, set())

        if val_required:
            diff["missing_required"][cls] = sorted(val_required)
        if val_optional:
            diff["missing_optional"][cls] = sorted(val_optional)

    # --- 3. Extra classes in Markdown not in validation dicts ---
    for cls in md_classes - validation_classes:
        md_required = set(extracted_tables[cls].get("required", []))
        md_optional = set(extracted_tables[cls].get("optional", []))

        if md_required:
            diff["extra_required"][cls] = sorted(md_required)
        if md_optional:
            diff["extra_optional"][cls] = sorted(md_optional)

    return diff

def get_table_diffs(md_path: Path):
    md_text = md_path.read_text(encoding="utf-8")
    tokens = parse_markdown(md_text, tables=True)
    extracted_tables = extract_property_tables(tokens)

    #from pprint import pp
    #pp(extracted_tables)

    diffs = diff_property_tables(extracted_tables)
    return diffs

def main():
    diffs = get_table_diffs(MD_PATH)
    missing = diffs["missing_classes"].copy()
    # Process and write output
    new_md = process_markdown(MD_PATH, diffs=diffs)
    
    OUT_PATH.write_text(new_md, encoding="utf-8")

    print(f"Updated markdown written to {OUT_PATH}")
    return diffs

if __name__ == "__main__":
    from pprint import pp
    pp(main())
