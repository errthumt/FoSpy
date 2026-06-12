from pandas import DataFrame
from ..engines import ENGINES
from ....config import values as cfg

X_LABEL = cfg.diffraction.x_label
class PhaseMatcher:
    def __init__(self, exp_2theta, exp_int, cif_dict, **kwargs):
        from .match import merge_frames
        frames = {'exp':DataFrame({X_LABEL:exp_2theta, "int":exp_int})}
        
        for name, cif in cif_dict.items():
            engine = cif.new_engine(engine_name='pymatgen', **kwargs)
            frames[name] = engine.get_pattern()
        
        self.frame = merge_frames(x_name=X_LABEL, normalize=True, interpolate=False, **frames)

    def match_peaks(self, **kwargs):
        pass








