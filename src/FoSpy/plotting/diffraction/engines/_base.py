import pandas as pd

class CIF_engine:
    def _to_frame(self, two_theta, intensity):
        return pd.DataFrame({'two_theta':two_theta, 'intensity':intensity})