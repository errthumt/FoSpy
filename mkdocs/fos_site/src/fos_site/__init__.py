from . import check_tables, run_example, build_nav, fos_to_md, copy_md

class FileMismatchError(Exception):
    pass

def build_full_site(automated=False):
    diffs = check_tables.update_tables_report_diffs()

    for diff in diffs.values():
        if len(diff) > 0:
            from pprint import pformat
            report = f"Mismatch in property tables:\n{pformat(diffs)}"

            if not automated:
                from warnings import warn
                warn(report, UserWarning)
                input("Press enter to continue...")
                break
            else:
                raise FileMismatchError(report)

    copy_md.copy_all()
    run_example.extract_and_run(figures=False)
    fos_to_md.generate_fos_pages()
    build_nav.generate_yml()

def build_full_site_cli():
    build_full_site(automated=True)

