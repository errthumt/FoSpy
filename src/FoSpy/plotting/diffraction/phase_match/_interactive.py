def check_for_interactive(interactive, kw):
    if isinstance(interactive, bool):
        return interactive
    elif isinstance(interactive, str):
        return interactive == kw
    elif isinstance(interactive, list):
        return kw in interactive

def get_find_sliders(find_cfg, intensity_col):
    return {
    "height": {
        "type": "range", "label": "Peak Height", "min": 0, "max": max(intensity_col), "default": find_cfg["height"]
    },
    "threshold": {
        "type": "range", "label": "Threshold", "min": 0, "max": 1, "default": find_cfg["threshold"]
    },
    "distance": {
        "type": "scalar", "label": "Min Distance (samples)", "min": 1, "max": 200, "default": find_cfg["distance"], "digits": 0
    },
    "prominence": {
        "type": "range", "label": "Prominence", "min": 0, "max": max(intensity_col), "default": find_cfg["prominence"]
    },
    "width": {
        "type": "range", "label": "Width (samples)", "min": 0, "max": len(intensity_col), "default": find_cfg["width"], "digits": 0
    },
    "wlen": {
        "type": "scalar", "label": "Window Length", "min": 2, "max": len(intensity_col), "default": find_cfg["wlen"], "digits": 0
    },
    "rel_height": {
        "type": "scalar", "label": "Relative Height", "min": 0, "max": 1, "default": find_cfg["rel_height"]
    },
    "plateau_size": {
        "type": "range", "label": "Plateau Size", "min": 0, "max": 200, "default": find_cfg["plateau_size"], "digits": 0
    },
}


# -------------------------------
# Layout constants for UI elements
# -------------------------------
LEFT_MARGIN = 0.02
RIGHT_MARGIN = 0.02

START_Y = 0.1
PANEL_START = 0.70
PANEL_W = 1.0 - PANEL_START
PADDING = 0.02
CHECK_X      = PANEL_START+PADDING
CHECK_W      = 0.06
SLIDER_X     = CHECK_X + CHECK_W + PADDING
SLIDER_W     = 1.0 - SLIDER_X - PADDING
LABEL_LSHIFT = (CHECK_W + 2*PADDING) / SLIDER_W
ROW_H        = 0.03

ROW_SPACING  = 0.05

OK_BTN_W     = 0.20
OK_BTN_H     = 0.05

def _get_label_offset(slider_width):
    offset = 2*PADDING + CHECK_W

    offset = offset / slider_width
    return offset

def _count_sliders(specs):
    total = 0
    for sp in specs.values():
        if sp["type"] == "scalar":
            total += 1
        elif sp["type"] == "range":
            total += 2
    return total

class SliderPlot():
    def __init__(self, figsize=(10,6), title="Interactive Plot", specs={}, cfg={}):
        from matplotlib import pyplot as plt
        from matplotlib.widgets import Slider

        self.specs = specs
        self.labels = {sp['label']: k for k, sp in specs.items()}
        self.sl_rows = _count_sliders(specs)
        self.row_height = 1.0 / self.sl_rows

        self.cfg = cfg

        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ax.set_title(title)
        

        self.sliders = {}
        self.checks = {}
        self.textboxes = {}

        self.panel_ax = self.fig.add_axes([PANEL_START, START_Y, PANEL_W, 1-START_Y])
        self.panel_ax.set_title("Parameters", fontsize=16)
        self.panel_ax.set_axis_off()
        self.panel_width = self.panel_ax.get_window_extent().width
        self.pilot_slider = Slider(self.panel_ax.inset_axes([0, 0, 1, 1]), "", 0, 1, valinit=0, dragging=False)
        self.max_label_width = 0.0

        self.ypos = 0

        for name, spec in specs.items():
            if spec["type"] == "scalar":
                ypos = self.add_slider(name)
            elif spec["type"] == "range":
                ypos = self.add_slider(name, range_type="min")
                ypos = self.add_slider(name, range_type="max")

        self.pilot_slider.disconnect_events()
        for vis in (
            self.pilot_slider.ax,
            self.pilot_slider.label,
            self.pilot_slider.valtext,
            self.pilot_slider.poly
        ):
            vis.set_visible(False)

        fig_width = self.fig.get_window_extent().width
        label_width = self.max_label_width / fig_width
        label_width += (3*PADDING + CHECK_W) * PANEL_W
        plt.subplots_adjust(left=LEFT_MARGIN, right=PANEL_START-label_width)


        try:
            self.update_plot()
        except:
            pass

    def disable_slider(self, spec_name):
        sl = self.sliders[spec_name]

        sl.active = False
        # sl.eventson = False
        self.update_plot()


    def enable_slider(self, spec_name):
        sl = self.sliders[spec_name]

        sl.active = True
        # sl.eventson = True
        self.update_plot()

    
    def toggle_slider(self, spec_name):
        if self.checks[spec_name].get_status()[0]:
            self.enable_slider(spec_name)
        else:
            self.disable_slider(spec_name)

    def update_cfg(self):
        for name, spec in self.specs.items():
            if spec["type"] == "scalar":
                enabled = self.checks[name].get_status()[0]
                self.cfg[name] = self.sliders[name].val if enabled else None

            elif spec["type"] == "range":
                lo_enabled = self.checks[name + "_min"].get_status()[0]
                hi_enabled = self.checks[name + "_max"].get_status()[0]

                lo = self.sliders[name + "_min"].val if lo_enabled else None
                hi = self.sliders[name + "_max"].val if hi_enabled else None

                self.cfg[name] = [lo, hi]

    def update_plot(self, val=None):
        self.update_cfg()
        # self.ax.draw_artist(self.ax.patch)
        # self.fig.canvas.draw_idle()

    def update_slider(self, spec_name):
        slider = self.sliders[spec_name]
        textbox = self.textboxes[spec_name]

        if spec_name.split("_")[-1] in ["min", "max"]:
            spec_name = spec_name[:-4]
        digits = self.specs[spec_name].get("digits", 2)

        def update(val, slider=slider, textbox=textbox, digits=digits):
            try:
                if not slider.active:
                    raise ValueError
                slider.set_val(float(val))
                self.update_plot()
            except ValueError:
                textbox.set_val(f"{slider.val:.{digits}f}")

        return update
    
    def update_textbox(self, spec_name):
        textbox = self.textboxes[spec_name]
        slider = self.sliders[spec_name]
        if spec_name.split("_")[-1] in ["min", "max"]:
            spec_name = spec_name[:-4]
        digits = self.specs[spec_name].get("digits", 2)
        def update(val, slider=slider, textbox=textbox, digits=digits):
            if not slider.active:
                slider.set_val(float(textbox.val))
            else:
                textbox.set_val(f"{slider.val:.{digits}f}")
                self.update_plot()
        return update

    def add_slider(self, spec_name, range_type=None):
        from matplotlib.widgets import Slider, CheckButtons, TextBox
        from mpl_toolkits.axes_grid1.inset_locator import inset_axes

        sp = self.specs[spec_name]
        label = sp['label']

        if range_type is None:
            default = sp['default']
        elif range_type == 'min':
            default = sp['default'][0]
            spec_name = spec_name + "_min"
            label = label + " (min)"
        elif range_type == 'max':
            default = sp['default'][1]
            spec_name = spec_name + "_max"
            label = label + " (max)"

        enabled = default is not None
        check_ax = self.panel_ax.inset_axes([-CHECK_W-PADDING, self.ypos, CHECK_W, self.row_height/2])
        check = CheckButtons(check_ax, [spec_name], [enabled],label_props={'fontsize':[14]},)
        check.labels[0].set_visible(False)
        self.checks[spec_name] = check

        digits = sp.get('digits', 2)
        self.pilot_slider.valtext.set_text(f"{sp['max']:.{digits}f}")
        text_width = self.pilot_slider.valtext.get_window_extent().width
        text_width = text_width / self.panel_width
        tb_width = text_width + PADDING

        if default is None:
            default = sp['max'] if range_type=='max' else sp['min']

        sl_width = 1-tb_width-2*PADDING
        ax_sl = self.panel_ax.inset_axes([0, self.ypos, sl_width, self.row_height/2])
        slider = Slider(ax_sl,label, sp['min'], sp['max'], valinit=default, valstep=(10**-digits), dragging=True)
        slider.valtext.set_visible(False)
        self.sliders[spec_name] = slider

        label_width = slider.label.get_window_extent().width
        if label_width > self.max_label_width:
            self.max_label_width = label_width

        label_offset = _get_label_offset(sl_width)
        slider.label.set_position((-label_offset, 0.5))

        ax_text = self.panel_ax.inset_axes([1.0-tb_width-PADDING, self.ypos, tb_width, self.row_height/2])
        textbox = TextBox(ax_text, "", initial=f"{slider.val:.{sp.get('digits', 2)}f}")
        self.textboxes[spec_name] = textbox

        slider.on_changed(self.update_textbox(spec_name))
        textbox.on_submit(self.update_slider(spec_name))
        check.on_clicked(self.toggle_slider)

        slider.active = enabled
        

        self.ypos += self.row_height

    def main_loop(self):
        from matplotlib import pyplot as plt
        self.update_plot()
        self.fig.canvas.draw_idle()
        plt.show()




class PeakFinder(SliderPlot):
    def __init__(self, exp_corrected, exp_index, cfg={}, **kwargs):
        specs = get_find_sliders(cfg, exp_corrected)
        super().__init__(specs=specs, cfg=cfg, **kwargs)

        from matplotlib.collections import LineCollection

        self.exp_corrected = exp_corrected
        self.exp_index = exp_index

        self.sticks = LineCollection([], colors='r')
        self.ax.add_collection(self.sticks)

        self.peaks, self.widths = None, None

        self.ax.plot(self.exp_index, self.exp_corrected, color='b', alpha=0.5)
        self.ax.set_xlim(min(self.exp_index), max(self.exp_index))

        try:
            self.update_plot()
        except:
            pass

    def update_sticks(self):
        from ._utils import rows_to_2th
        from .match import unpack_peaks

        self.peaks, self.widths = unpack_peaks(self.exp_corrected, "widths", **self.cfg)

        peaks_list = [int(x) for x in self.peaks]
        intensity_list = [self.exp_corrected[x] for x in peaks_list]
        peaks_2th = rows_to_2th(self.exp_index, peaks_list)

        segments = [ [(x, 0), (x, y)] for x, y in zip(peaks_2th, intensity_list)]
        self.sticks.set_segments(segments)
        
        self.ax.draw_artist(self.sticks)
        self.fig.canvas.blit(self.ax.bbox)
        #self.fig.canvas.draw_idle()
    
    def update_plot(self, val=None):
        super().update_plot(val)
        self.update_sticks()

    def main_loop(self):
        super().main_loop()
        return self.peaks, self.widths
