from textwrap import dedent

def generate_json_stubs(download_dir, maps_dir):
    from FoSpy._dev.testing.map_guides import EXPECTED_FN, REQUIRED_FN
    
    pages = {
        "optional": EXPECTED_FN + ".json",
        "required": REQUIRED_FN + ".json",
    }

    for page, fn in pages.items():
        fp = download_dir / fn
        rel_fp = fp.relative_to(maps_dir, walk_up=True)
        preamble = dedent(
            f"""
            # FoSpy JSON Map Guide - {page}

            [Download Here.]({rel_fp.as_posix()}) If your browser does not download, save the page directly (usually with Ctrl + S).

            [Return to Mapping Tutorial](./index.md)

            ```JSON
            """
        )

        with open(fp, "r") as f:
            json_txt = f.read()

        with open(maps_dir / f"{page}.md", "w", encoding="utf-8") as f:
            f.write(preamble)
            f.write(json_txt)
            f.write("\n```\n")