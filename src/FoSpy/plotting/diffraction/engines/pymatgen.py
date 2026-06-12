from ._base import CIF_engine

class pymatgen_engine(CIF_engine):
    def __init__(self, cif_path, **kwargs):
        from pymatgen.analysis.diffraction.xrd import XRDCalculator
        from pymatgen.core.structure import Structure
        self.structure = Structure.from_file(cif_path)
        self.sim = XRDCalculator()
    
    def get_pattern(self,**kwargs):
        import numpy as np
        from ....config import values as cfg

        params = super().get_pattern(**kwargs)
        
        peaks = self.get_peaks(**kwargs)

        step = params['two_theta_step']
        tth_range = params['two_theta_range']
        

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
    
    def get_peaks(self,**kwargs):
        params = super().get_pattern(**kwargs)
        tth_range = params['two_theta_range']
        normalize = params['normalize']


        pattern = self.sim.get_pattern(self.structure, two_theta_range=tth_range, scaled = False)

        if normalize:
            pattern.y = pattern.y / max(pattern.y)

        peaks = tuple((x, y) for x, y in zip(pattern.x, pattern.y))
        return peaks
