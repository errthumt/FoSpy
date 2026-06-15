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

    def _check_for_interactive(self, interactive, kw):
        if isinstance(interactive, bool):
            return interactive
        elif isinstance(interactive, str):
            return interactive == kw
        elif isinstance(interactive, list):
            return kw in interactive

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
        self.find_baseline(interactive=interactive)
        interactive = self._check_for_interactive(interactive, "find_peaks")
        
        exp_corrected = self.frames['exp']['corrected'].to_numpy()

        from .match import unpack_peaks

    
        find_cfg = self.find_cfg
        peaks, widths = unpack_peaks(exp_corrected, "widths",**find_cfg)
        if not interactive:
            return peaks, widths
        
        from matplotlib import pyplot as plt
        from matplotlib.widgets import Slider, Button, CheckButtons, TextBox
        from matplotlib.collections import LineCollection
        from ._utils import plot_stick_at_x, rows_to_2th, get_find_sliders
        exp_index = self.frames['exp'].index.to_numpy()

        slider_specs = get_find_sliders(find_cfg, exp_corrected)

        # -------------------------------
        # Layout constants for UI elements
        # -------------------------------
        START_Y = 0.1
        SLIDER_START_X = 0.70
        PADDING = 0.01
        CHECK_X      = SLIDER_START_X+PADDING
        CHECK_W      = 0.03
        SLIDER_X     = CHECK_X + CHECK_W + PADDING
        SLIDER_W     = 1.0 - SLIDER_X - PADDING
        LABEL_LSHIFT = (CHECK_W + 2*PADDING) / SLIDER_W
        ROW_H        = 0.03
        ROW_SPACING  = 0.05

        OK_BTN_W     = 0.20
        OK_BTN_H     = 0.05

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title("Peak Assignment for baseline-adjusted intensity")
        plt.subplots_adjust(right=SLIDER_START_X, left=PADDING)
        self.frames['exp'].plot(ax=ax, y='corrected')

        slider_axes = {}
        sliders = {}
        checks = {}
        stick_lines = []
        sticks = LineCollection([], colors='b')
        ax.add_collection(sticks)


        def disable(slider):
            slider.eventson = False
            slider.active = False
            slider.ax.set_alpha(0.3)


        def enable(slider):
            slider.eventson = True
            slider.active = True
            slider.ax.set_alpha(1.0)

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
            intensity_list = [exp_corrected[x] for x in peaks_list] #exp_corrected[x]
            peaks_2th = rows_to_2th(exp_index, peaks_list)

            # for x in peaks_2th:
            #     stick_lines.append(
            #         plot_stick_at_x(x, exp_index, exp_corrected, ax=ax, color='b')
            #     )

            segments = [ [(x, 0), (x, y)] for x, y in zip(peaks_2th, intensity_list)]

            sticks.set_segments(segments)

            # fig.canvas.draw_idle()
            ax.draw_artist(ax.patch)
            ax.draw_artist(sticks)
            fig.canvas.blit(ax.bbox)


        def new_slider(label, fig, spec, ypos, min_val, max_val, default, typ, slider_key):
            ax_check = fig.add_axes([CHECK_X, ypos, CHECK_W, ROW_H])
            check = CheckButtons(ax_check, [slider_key], [default is not None])
            check.labels[0].set_visible(False)

            ax_slider = fig.add_axes([SLIDER_X, ypos, SLIDER_W, ROW_H])
            slider = Slider(ax_slider, label, min_val, max_val, valinit=max_val, dragging=False)
            slider.valtext.set_text(f"{slider.val:.{spec.get('digits', 2)}f}")

            text_width = slider.valtext.get_window_extent().width
            fig_width = fig.get_window_extent().width
            text_width = text_width / fig_width

            tb_width = text_width+PADDING

            ax_text = fig.add_axes([1.0-tb_width-PADDING, ypos, tb_width, ROW_H])
            textbox = TextBox(ax_text, "", initial=slider.valtext.get_text())

            slider.valtext.set_visible(False)

            def update_slider(text, slider=slider, textbox=textbox, digits=spec.get("digits", 2)):
                try:
                    if not slider.eventson:
                        raise ValueError
                    slider.set_val(float(text))
                    update()
                except ValueError:
                    textbox.set_val(f"{slider.val:.{digits}f}")

            def update_textbox(val, textbox=textbox,digits=spec.get("digits", 2)):
                textbox.set_val(f"{val:.{digits}f}")
                update()



            slider.ax.set_position([SLIDER_X, ypos, SLIDER_W-tb_width-PADDING, ROW_H])


            if default is not None:
                slider.set_val(default)
            else:
                disable(slider)
                if typ in ("min", "scalar"):
                    slider.set_val(min_val)
                else:
                    slider.set_val(max_val)
            
            ypos += ROW_SPACING

            slider.on_changed(update_textbox)
            textbox.on_submit(update_slider)

            return slider, check, ypos
        

        ypos = START_Y + OK_BTN_H + ROW_SPACING

        for name, spec in slider_specs.items():

            if spec["type"] == "scalar":

                sliders[name], checks[name], ypos = new_slider(
                    spec["label"], fig, spec, ypos, spec["min"], 
                    spec["max"], spec["default"], "scalar", name)


            elif spec["type"] == "range":
                lo, hi = spec["default"] if spec["default"] else (None, None)

                lo_name = name + "_min"
                lo_label =spec["label"] + " (min)"
                sliders[lo_name], checks[lo_name], ypos = new_slider(
                    lo_label, fig, spec, ypos, spec["min"], 
                    spec["max"], lo, "min", lo_name)
                
                hi_name = name + "_max"
                hi_label =spec["label"] + " (max)"
                sliders[hi_name], checks[hi_name], ypos = new_slider(
                    hi_label, fig, spec, ypos, spec["min"], 
                    spec["max"], hi, "max", hi_name)



        def toggle_slider(label):
            if label in sliders:
                print(f"toggling {label}")
                enabled = not sliders[label].eventson
                if enabled:
                    enable(sliders[label])
                else:
                    disable(sliders[label])
            
            update()



        

        def accept(event):
            self.find_cfg = find_cfg
            plt.close(fig)

        for check in checks.values():
            check.on_clicked(toggle_slider)

        max_label_width = 0
        for s in sliders.values():
            s.label.set_position((-LABEL_LSHIFT, .5))
            label_width = s.label.get_window_extent().width
            if label_width > max_label_width:
                max_label_width = label_width

        fig_width = fig.get_window_extent().width
        max_label_width = max_label_width / fig_width
        full_margin = SLIDER_START_X - PADDING - max_label_width
        plt.subplots_adjust(right=full_margin)

        ok_center = (1+full_margin) / 2
        ok_x = ok_center - OK_BTN_W/2
        ok_ax = fig.add_axes([ok_x, START_Y, OK_BTN_W, OK_BTN_H])
        ok_button = Button(ok_ax, "OK")
        ok_button.on_clicked(accept)

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
        interactive = self._check_for_interactive(interactive, "baseline")

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
        











