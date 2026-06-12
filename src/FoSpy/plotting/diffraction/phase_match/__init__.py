from pandas import DataFrame
from ..engines import ENGINES
from ....config import values as cfg
class PhaseMatcher(DataFrame):
    def __init__(self, exp_2theta, exp_int, *cif_attachments, engine=None,**kwargs):
        from .match import merge_frames
        super().__init__({
            "two_theta":exp_2theta, "intensity":exp_int
        })

        if engine is None:
            engine = cfg.diffraction.engine.default

        default_engine_parameters = cfg.

        self.engines = []





