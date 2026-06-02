from fos_site import check_tables, run_example, build_nav, fos_to_md

if __name__ == "__main__":
    from pprint import pp
    pp(check_tables.update_tables_report_diffs())
    run_example.extract_and_run(figures=False)
    fos_to_md.generate_fos_pages()
    build_nav.generate_yml()