from pathlib import Path

MD_PATH = Path("mkdocs/docs/expected/index.md")
#OUT_PATH = Path("mkdocs/scripts/required_tables/index_with_links.md")
OUT_PATH = MD_PATH
TEMPLATE_PATH = Path("mkdocs/build_scripts/class_template.md")

def update_tables_report_diffs(delay=False):
    from .._utils import ch2repo
    ch2repo()

    from .helpers import get_table_diffs, process_markdown

    diffs = get_table_diffs(MD_PATH)

    def update():
        ch2repo()
        # Process and write output
        new_md = process_markdown(MD_PATH, diffs=diffs, temp_path=TEMPLATE_PATH)
        
        OUT_PATH.write_text(new_md, encoding="utf-8")

        print(f"Updated markdown written to {OUT_PATH}")
    if delay:
        return diffs, update
    return diffs
