import pandas as pd

class CIF_engine:
    def _to_frame(self, two_theta, intensity):
        from ....config import values as cfg
        x_label = cfg.diffraction.x_label
        return pd.DataFrame({x_label:two_theta, 'int':intensity})
    
    def get_pattern(self, **kwargs):
        from ....config import values as cfg

        params = cfg.diffraction.pattern_parameters().copy()
        params.update(kwargs)
        return params