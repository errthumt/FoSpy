from .cif2xrd import cif2xrd_engine
from .dans_diffraction import DansEngine

ENGINES = {"cif2xrd": cif2xrd_engine, "dans-diffraction": DansEngine}
