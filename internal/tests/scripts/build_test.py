from fos_site._utils import ch2repo
from fos_site import build_full_site

if __name__ == "__main__":
    import os, pathlib
    os.chdir(pathlib.Path(__file__).parent)
    ch2repo()
    build_full_site()