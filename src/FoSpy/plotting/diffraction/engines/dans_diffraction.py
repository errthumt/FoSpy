
from ._base import CIF_engine
available = True
try:
    import Dans_Diffraction as ddf #type: ignore
except ImportError:
    available = False
class Engine(CIF_engine):
    def __init__(self, cif_path, **kwargs):
        if not available:
            raise ImportError("Diffraction Engine: Dans_Diffraction could not be imported. Please install it using pip install Dans_Diffraction")
        self.xtl = ddf.Crystal(cif_path)
        self.sim =  self.xtl.Scatter
        self.sim.setup_scatter(**kwargs)

    def get_pattern(self, two_theta_range:tuple=None,**kwargs):
        two_theta, intensity, reflections = self.sim.powder(**kwargs)
        return self._to_frame(two_theta, intensity)
