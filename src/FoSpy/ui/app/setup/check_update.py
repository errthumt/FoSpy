import subprocess
from packaging.requirements import Requirement

from .._utils import ASSETS

def check_packages():
    frozen = _load_frozen()
    compatible = _load_compiled(ASSETS["compatible packages"])

    incompatible = set(frozen.keys()) - set(compatible.keys())
    incompatible = {name: frozen[name] for name in incompatible}

    if incompatible:
        print("Incompatible packages found:")
        for name, ver in incompatible.items():
            print(f"* {name}=={ver}")



def _load_frozen():
    out = subprocess.check_output(["pip", "freeze"], text=True)
    pkgs = {}
    for line in out.splitlines():
        line = line.strip()
        if "==" in line:
            name, ver = line.split("==", 1)
            pkgs[name.lower()] = ver

    return pkgs

def _load_compiled(path):
    pkgs = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "==" not in line:
                continue

            name, ver = line.split("==", 1)
            name = name.split(";")[0].strip().lower()
            pkgs[name] = ver

    return pkgs
