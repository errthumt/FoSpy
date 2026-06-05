from . import check_tables, run_example, build_nav, fos_to_md, internal
import argparse

class FileMismatchError(Exception):
    pass

def build_full_site(deploy=False, figures=False):
    diffs = check_tables.update_tables_report_diffs()

    for diff in diffs.values():
        if len(diff) > 0:
            from pprint import pformat
            report = f"Mismatch in property tables:\n{pformat(diffs)}"

            if not deploy:
                from warnings import warn
                warn(report, UserWarning)
                input("Press enter to continue...")
                break
            else:
                raise FileMismatchError(report)

    internal.copy_md.copy_all()
    internal.package_installers.pkg_all()
    
    run_example.extract_and_run(figures=figures)
    fos_to_md.generate_fos_pages()
    build_nav.generate_yml()

def build_full_site_cli():
    parser = argparse.ArgumentParser(description="Rebuild Docs Site")
    parser.add_argument("--deploy", action="store_true", help="Raise error instead of warning on property table mismatch. Prevents deploying mismatched site. (Default: False)")
    parser.add_argument("--figures", action="store_true", help="Generate figures in example code. (Default: False)")
    parser.set_defaults(on_deploy=False)
    parser.set_defaults(figures=False)
    args = parser.parse_args()
    build_full_site(deploy=args.deploy, figures=args.figures)

