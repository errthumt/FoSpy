from . import fos_to_md, build_nav, run_example

def build_site():
    run_example.main()
    fos_to_md.main()
    build_nav.main()

