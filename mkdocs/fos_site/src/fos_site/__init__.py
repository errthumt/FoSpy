from . import build_nav

from . import fos_to_md

from . import run_example

def build_site():
    run_example.main()
    fos_to_md.main()
    build_nav.generate_yml()

