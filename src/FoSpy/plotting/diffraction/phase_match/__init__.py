from pandas import DataFrame
from ..engines import ENGINES
from ....config import values as cfg
class PhaseMatcher:
    def __init__(self, exp_2theta, exp_int, cif_dict, engine=None, x_name="two_theta", **kwargs):
        from .match import merge_frames
        self.x_name = x_name
        df = DataFrame({
            "two_theta":exp_2theta, "intensity":exp_int
        })

        if engine is None:
            engine = cfg.diffraction.engine.default

        engine_parameters = cfg.diffraction.engines.engine_defaults[engine].to_dict()
        engine_parameters.update(kwargs)
        self.engine_cls = ENGINES[engine]

        self.engines = {k:self.engine_cls(cif._get_filepath(), **engine_parameters) for k, cif in cif_dict.items()}

        frames = {"exp":df,
                  **{name: engine.get_pattern() for name, engine in self.engines.items()}}
        
        self.frame = merge_frames(x_name=x_name, normalize=False, **frames)

    def match_peaks(self, **kwargs):
        pass








