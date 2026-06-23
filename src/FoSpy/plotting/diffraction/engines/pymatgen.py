from ._base import CIF_engine
from ....config import values as cfg

class Engine(CIF_engine):
    def __init__(self, cif_path, **kwargs):
        from pymatgen.analysis.diffraction.xrd import XRDCalculator
        from pymatgen.core.structure import Structure
        self.structure = Structure.from_file(cif_path)
        self.sim = XRDCalculator()
    
    def get_pattern(self,**kwargs):
        import numpy as np

        pattern_config = cfg.get("diffraction.pattern_parameters")
        pattern_config.update(kwargs)

        step = pattern_config.pop('two_theta_step')
        tth_range = pattern_config['two_theta_range']
        
        peaks = self.get_peaks(**pattern_config)

        two_theta = []
        intensity = []
        for (x,y) in peaks:
            two_theta.append(step*round(x/step))
            intensity.append(y)


        frame =  self._to_frame(two_theta, intensity)
        x_min, x_max = tth_range
        grid = np.arange(x_min, x_max+step, step)

        frame = (frame.
                 set_index(cfg.diffraction.x_label).
                 reindex(grid).
                 fillna(0).
                 reset_index())
        return frame
    
    def get_peaks(self,two_theta_range=None, normalize=None):

        if two_theta_range is None:
            two_theta_range = cfg.get("diffraction.pattern_parameters.two_theta_range")

        if normalize is None:
            normalize = cfg.get("diffraction.pattern_parameters.normalize")


        pattern = self.sim.get_pattern(self.structure, two_theta_range=two_theta_range, scaled = False)

        if normalize:
            pattern.y = pattern.y / max(pattern.y)

        peaks = tuple((x, y) for x, y in zip(pattern.x, pattern.y))
        return peaks
