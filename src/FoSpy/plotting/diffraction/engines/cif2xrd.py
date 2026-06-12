from cif2xrd.pattern import simPattern
from .pymatgen import pymatgen_engine

class cif2xrd_engine(pymatgen_engine):
    def __init__(self, cif_path, **kwargs):
        self.sim = simPattern(cif_path, **kwargs)
    def get_pattern(self,two_theta_range:tuple=None, **kwargs):
        self.sim.set_parameters(**kwargs)
        return self._to_frame(self.sim.two_theta, self.sim.intensity)