from pandas import DataFrame


from ..engines import ENGINES
from ....config import values as cfg
from ._interactive import check_for_interactive

X_LABEL = cfg.diffraction.x_label
class PhaseMatcher:
    def __init__(self, exp_2theta, exp_int, cif_dict):

        self.baseline_cfg = cfg.get("diffraction.baseline")
        self.find_cfg = cfg.get("diffraction.find_peaks")

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
    
    def find_peaks(self, interactive=False, **interactive_kwargs):
        self.find_baseline(interactive=interactive)
        interactive = check_for_interactive(interactive, "find_peaks")
        
        exp_corrected = self.frames['exp']['corrected'].to_numpy()

        from .match import unpack_peaks

    
        find_cfg = self.find_cfg
        if not interactive:
            return unpack_peaks(exp_corrected, "widths",**find_cfg)

        from ._interactive import PeakFinder

        interactive_kwargs.setdefault('title', "Baseline-Corrected Peak Finder")
        if interactive_kwargs['title'].startswith("+"):
            suffix = interactive_kwargs['title'][1:]
            interactive_kwargs['title'] = f"Baseline-Corrected Peak Finder\n{suffix}"

        peak_finder = PeakFinder(exp_corrected, self.frames['exp'].index, cfg=find_cfg, **interactive_kwargs)
        return peak_finder.main_loop()
        



    
    def plot_matches(self, cif_name, ax=None, show=False):
        import numpy as np
        from matplotlib import pyplot as plt
        from ._utils import plot_stick_at_x

        matchset = self.match_peaks()[cif_name]
        peak_list = self.cifs[cif_name].get_peaks()

        peaks_x = np.array([x for (x, y) in peak_list])
        peaks_y = np.array([y for (x, y) in peak_list])

        if ax is None:
            fig, ax = plt.gcf(), plt.gca()
        else:
            fig = ax.get_figure()

        self.frames['exp'].plot(ax=ax)

        for _, x_matches in matchset['matches']:
            for x in x_matches:
                plot_stick_at_x(x, peaks_x, peaks_y, ax=ax, color='g')

        for missing in matchset['missing']:
            plot_stick_at_x(missing, peaks_x, peaks_y, ax=ax, color='r')

        if show:
            plt.show()

        return fig, ax
    
    def find_baseline(self, interactive=False):
        interactive = check_for_interactive(interactive, "baseline")

        from pybaselines import Baseline

        exp_frame = self.frames['exp']
        fitter = Baseline()

        lam = self.baseline_cfg['smoothing_lam']

        exp_int = exp_frame['int']

        def set_baseline(to_lam):
            baseline, _ = fitter.arpls(
                exp_frame['int'].to_numpy(),
                lam=to_lam
            )
            exp_frame['baseline'] = baseline
            exp_frame['corrected'] = exp_int - baseline

            return baseline
        
        set_baseline(lam)

        if not interactive:
            return

        from matplotlib import pyplot as plt
        from matplotlib.widgets import Slider, Button
        import numpy as np

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title("Interactive Baseline Adjustment")

        plt.subplots_adjust(bottom=0.25)

        x = exp_frame.index

        exp_line, = ax.plot(x, exp_frame['int'], label='Experimental')
        base_line, = ax.plot(x, exp_frame['baseline'], label='Baseline')

        ax.legend()

        slider_ax = plt.axes([0.15, 0.10, 0.65, 0.03])

        # Use log10(lambda) because lambda spans many orders of magnitude
        loglam0 = np.log10(lam)

        lam_slider = Slider(
            slider_ax,
            r'log$_{10}(\lambda)$',
            2,      # 1e2
            10,     # 1e10
            valinit=loglam0,
        )

        button_ax = plt.axes([0.83, 0.08, 0.10, 0.06])
        ok_button = Button(button_ax, 'OK')

        def update(val):
            lam = 10**lam_slider.val

            baseline = set_baseline(lam)

            base_line.set_ydata(baseline)

            ax.relim()
            ax.autoscale_view()

            fig.canvas.draw_idle()

        def accept(event):
            self.baseline_cfg['smoothing_lam'] = 10**lam_slider.val
            plt.close(fig)

        lam_slider.on_changed(update)
        ok_button.on_clicked(accept)

        plt.show()

        return



        
            
        





    
    # def plot_matches(self):
        











