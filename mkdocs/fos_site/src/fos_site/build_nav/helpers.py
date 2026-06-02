def build_full_nav(tree: dict) -> list:
    """
    Convert nested dict structure from full_stubs into MkDocs nav list.
    Produces ONLY {name: path} or {folder: [...]}, never bare paths.
    """
    nav_list = []

    # Files directly in this folder: "." maps to {page_name: path}
    files = tree.get(".", {})
    file_items = list(files.items())  # [(page_name, path), ...]

    # Subfolders
    subfolders = [(k, v) for k, v in tree.items() if k != "."]

    # Case 1: folder contains exactly one file and no subfolders → collapse
    if len(file_items) == 1 and not subfolders:
        page_name, path = file_items[0]
        nav_list.append({page_name: path})
        return nav_list

    # Case 2: normal folder → list files first
    for page_name, path in file_items:
        nav_list.append({page_name: path})

    # Then subfolders
    for key, subtree in subfolders:
        subnav = build_full_nav(subtree)

        # Collapse subfolder if it contains exactly one {name: path}
        if len(subnav) == 1 and isinstance(subnav[0], dict):
            nav_list.append({key: subnav[0]})
        else:
            nav_list.append({key: subnav})

    return nav_list