from fos_site import check_tables, run_example

if __name__ == "__main__":
    check_tables.update_tables_report_diffs()
    run_example.extract_and_run()