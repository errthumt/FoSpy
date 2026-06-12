from pandas import DataFrame
from ..engines import ENGINES
from ....config import values as cfg

X_LABEL = cfg.diffraction.x_label
class PhaseMatcher:
    def __init__(self, exp_2theta, exp_int, cif_dict):
        from .match import merge_frames
        frames = {'exp':DataFrame({X_LABEL:exp_2theta, "int":exp_int}).set_index(X_LABEL)}
        x_min=min(exp_2theta)
        x_max=max(exp_2theta)
        for name, cif in cif_dict.items():
            engine = cif.new_engine(engine_name='pymatgen')
            frames[name] = engine.get_pattern().set_index(X_LABEL)
        self.cifs = cif_dict
        self.frames = frames

    def match_peaks(self):
        import numpy as np
        from .match import match_peaks
        from ._utils import rows_to_2th

        exp_frame = self.frames['exp']/self.frames['exp'].max()
        exp_data = exp_frame['int']
        exp_index = exp_frame.index

        matchsets = {}

        for name, cif in self.cifs.items():
            peak_list = cif.get_peaks()

            peak_idx = np.searchsorted(exp_index, [x for (x, y) in peak_list])

            matches = match_peaks(exp_data, peak_idx)

            matches = rows_to_2th(exp_index,matches)

            matchsets[name] = matches

        return matchsets
    
    def match_plot(self, cif_name):
        import numpy as np
        from matplotlib import pyplot as plt
        from ._utils import plot_stick_at_x

        matchset = self.match_peaks()[cif_name]
        peak_list = self.cifs[cif_name].get_peaks()

        peaks_x = np.array([x for (x, y) in peak_list])
        peaks_y = np.array([y for (x, y) in peak_list])

        fig, ax = plt.subplots()

        self.frames['exp'].plot(ax=ax)

        for _, x_matches in matchset['matches']:
            for x in x_matches:
                plot_stick_at_x(x, peaks_x, peaks_y, ax=ax, color='g')

        for missing in matchset['missing']:
            plot_stick_at_x(missing, peaks_x, peaks_y, ax=ax, color='r')

        plt.show()


        
            
        





    
    # def plot_matches(self):
        











