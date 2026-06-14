from pandas import DataFrame
from ..engines import ENGINES
from ....config import values as cfg

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
    
    def find_peaks(self, interactive=False):
        self.find_baseline(interactive=False)
        exp_corrected = self.frames['exp']['corrected'].to_numpy()

        from .match import unpack_peaks

    
        find_cfg = self.find_cfg
        peaks, widths = unpack_peaks(exp_corrected, "widths",**find_cfg)
        if not interactive:
            return peaks, widths
        
        from matplotlib import pyplot as plt
        from matplotlib.widgets import Slider, Button, CheckButtons
        from ._utils import plot_stick_at_x, rows_to_2th, get_find_sliders
        exp_index = self.frames['exp'].index.to_numpy()

        slider_specs = get_find_sliders(find_cfg, exp_corrected)

        # -------------------------------
        # Layout constants for UI elements
        # -------------------------------
        CHECK_X      = 0.74
        SLIDER_X     = 0.78
        SLIDER_W     = 0.20
        CHECK_W      = 0.03
        ROW_H        = 0.03
        ROW_SPACING  = 0.05
        RIGHT_MARGIN = 0.75
        OK_BTN_W     = 0.20
        OK_BTN_H     = 0.05
        OK_BTN_X     = 0.78

        ypos = 0.1

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title("Peak Assignment for baseline-adjusted intensity")
        plt.subplots_adjust(right=RIGHT_MARGIN)
        self.frames['exp'].plot(ax=ax, y='corrected')

        slider_axes = {}
        sliders = {}
        checks = {}

        for name, spec in slider_specs.items():

            if spec["type"] == "scalar":
                # Checkbox
                ax_check = fig.add_axes([CHECK_X, ypos, CHECK_W, ROW_H])
                checks[name] = CheckButtons(ax_check, [""], [spec["default"] is not None])

                # Slider
                ax_slider = fig.add_axes([SLIDER_X, ypos, SLIDER_W, ROW_H])
                init = spec["default"] if spec["default"] is not None else spec["min"]
                sliders[name] = Slider(ax_slider, spec["label"], spec["min"], spec["max"], valinit=init)

                if spec["default"] is None:
                    sliders[name].ax.set_alpha(0.3)
                    sliders[name].eventson = False

                ypos += ROW_SPACING

            elif spec["type"] == "range":
                lo, hi = spec["default"] if spec["default"] else (None, None)

                # --- MIN ---
                ax_check_min = fig.add_axes([CHECK_X, ypos, CHECK_W, ROW_H])
                checks[name + "_min"] = CheckButtons(ax_check_min, [""], [lo is not None])

                ax_slider_min = fig.add_axes([SLIDER_X, ypos, SLIDER_W, ROW_H])
                lo_init = lo if lo is not None else spec["min"]
                sliders[name + "_min"] = Slider(
                    ax_slider_min, spec["label"] + " (min)", spec["min"], spec["max"], valinit=lo_init
                )

                if lo is None:
                    sliders[name + "_min"].ax.set_alpha(0.3)
                    sliders[name + "_min"].eventson = False

                ypos += ROW_SPACING

                # --- MAX ---
                ax_check_max = fig.add_axes([CHECK_X, ypos, CHECK_W, ROW_H])
                checks[name + "_max"] = CheckButtons(ax_check_max, [""], [hi is not None])

                ax_slider_max = fig.add_axes([SLIDER_X, ypos, SLIDER_W, ROW_H])
                hi_init = hi if hi is not None else spec["max"]
                sliders[name + "_max"] = Slider(
                    ax_slider_max, spec["label"] + " (max)", spec["min"], spec["max"], valinit=hi_init
                )

                if hi is None:
                    sliders[name + "_max"].ax.set_alpha(0.3)
                    sliders[name + "_max"].eventson = False

                ypos += ROW_SPACING


        stick_lines = []

        def update(val=None):
            for name, spec in slider_specs.items():
                if spec["type"] == "scalar":
                    enabled = checks[name].get_status()[0]
                    find_cfg[name] = sliders[name].val if enabled else None

                elif spec["type"] == "range":
                    lo_enabled = checks[name + "_min"].get_status()[0]
                    hi_enabled = checks[name + "_max"].get_status()[0]

                    lo = sliders[name + "_min"].val if lo_enabled else None
                    hi = sliders[name + "_max"].val if hi_enabled else None

                    find_cfg[name] = [lo, hi]

            peaks, widths = unpack_peaks(exp_corrected, "widths", **find_cfg)

            for line in stick_lines:
                line.remove()
            stick_lines.clear()

            peaks_list = [int(x) for x in peaks]
            peaks_2th = rows_to_2th(exp_index, peaks_list)

            for x in peaks_2th:
                stick_lines.append(
                    plot_stick_at_x(x, exp_index, exp_corrected, ax=ax, color='b')
                )

            fig.canvas.draw_idle()


        def toggle_slider(label):
            for key, check in checks.items():
                if check.eventson:
                    enabled = check.get_status()[0]
                    if key in sliders:
                        sliders[key].eventson = enabled
                        sliders[key].ax.set_alpha(1.0 if enabled else 0.3)
                    break
            fig.canvas.draw_idle()


        ok_ax = fig.add_axes([OK_BTN_X, ypos + ROW_SPACING, OK_BTN_W, OK_BTN_H])
        ok_button = Button(ok_ax, "OK")

        def accept(event):
            self.find_cfg = find_cfg
            plt.close(fig)

        ok_button.on_clicked(accept)

        for check in checks.values():
            check.on_clicked(toggle_slider)

        for s in sliders.values():
            s.on_changed(update)

        update()
        plt.show()



    
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
        











