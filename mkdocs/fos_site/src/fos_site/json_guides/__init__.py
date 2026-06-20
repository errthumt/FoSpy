from FoSpy._dev.testing.map_guides import run as build_JSONs, SUB_DIR
from pathlib import Path
from .._utils import ch2repo
from .helpers import generate_json_stubs

MAPS_DIR = Path("mkdocs/docs/guides/maps")
DOWNLOAD_DIR = Path("mkdocs/docs/file_download") / SUB_DIR

def build_guides():
    ch2repo()
    build_JSONs(DOWNLOAD_DIR, open_result=False)
    generate_json_stubs(DOWNLOAD_DIR, MAPS_DIR)