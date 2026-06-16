from .pymatgen import Engine as Engine_pymatgen

available = True
try:
    from cif2xrd.pattern import simPattern
except ImportError as e:
    available = False

class Engine(Engine_pymatgen):
    def __init__(self, cif_path, **kwargs):
        if not available:
            raise ImportError("Diffraction engine cif2xrd is not installed. Install it with `pip install cif2xrd`")
        self.sim = simPattern(cif_path, **kwargs)
    def get_pattern(self,two_theta_range:tuple=None, **kwargs):
        self.sim.set_parameters(**kwargs)
        return self._to_frame(self.sim.two_theta, self.sim.intensity)