from . import cif2xrd, dans_diffraction, pymatgen

ENGINES = {
    "cif2xrd": cif2xrd.Engine, 
    "dans-diffraction": dans_diffraction.Engine,
    "pymatgen": pymatgen.Engine
}
