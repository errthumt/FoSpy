from .abstract import SliderPlot as AbstractSlider

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.collections import LineCollection

available = True

# -------------------------------
# Layout constants for UI elements
# -------------------------------
LEFT_MARGIN = 0.05
RIGHT_MARGIN = 0.02

START_Y = 0.2
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
OK_BTN_H     = START_Y / 2

def _get_label_offset(slider_width):
    offset = 2*PADDING + CHECK_W

    offset = offset / slider_width
    return offset

class SliderPlot(AbstractSlider):
    def __init__(self, figsize=(10,6), title="Interactive Plot", specs={}, cfg={}, x_label=None, y_label=None, x_ticks=True, y_ticks=True, backend='TkAgg'):
        
        try:
            matplotlib.use(backend)
        except Exception as e:
            from warnings import warn
            warn(f"Could not set matplotlib backend to {backend}. Using system default. "
                 f"Exception:\n{e}", RuntimeWarning)

        self.fig, self.ax = plt.subplots(figsize=figsize)

        super().__init__(specs=specs, cfg=cfg, x_label=x_label, y_label=y_label, x_ticks=x_ticks, y_ticks=y_ticks)

        

        #self.labels = {sp['label']: k for k, sp in specs.items()}

        self.row_height = 1.0 / self.sl_rows

        self.ax.set_title(title)

        self.panel_ax = self.fig.add_axes([PANEL_START, START_Y, PANEL_W, 1-START_Y])
        self.panel_ax.set_title("Parameters", fontsize=16)
        self.panel_ax.set_axis_off()
        self.panel_width = self.panel_ax.get_window_extent().width
        self.pilot_slider = Slider(self.panel_ax.inset_axes([0, 0, 1, 1]), "", 0, 1, valinit=0, dragging=False)
        self.max_label_width = 0.0

        self.ypos = 0

        # TODO: better group organization
        # temporary: unpack groups
        unpacked = {}
        for name, spec in specs.items():
            if spec["type"] == "group":
                grp_label = spec["label"]
                grp_name = name
                for nm, spc in spec["specs"].items():
                    spc["label"] = f"({grp_label}) {spc['label']}"
                    unpacked[f"{grp_name}_{nm}"] = spc
            else:
                unpacked[name] = spec

        specs = unpacked

        for name, spec in specs.items():
            if spec["type"] == "scalar":
                self.add_slider(name)
            elif spec["type"] == "range":
                self.add_slider(name, range_type="min")
                self.add_slider(name, range_type="max")

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

        ok_center = (1.0 + PANEL_START - label_width) / 2.0
        ok_start_x = ok_center - OK_BTN_W/2.0
        ok_start_y = START_Y / 4.0
        ok_ax = self.fig.add_axes([ok_start_x, ok_start_y, OK_BTN_W, OK_BTN_H])
        ok_ax.set_zorder(1000)
        self.ok_btn = Button(ok_ax, 'OK')
        self.ok_btn.on_clicked(self._ok_clicked)

        self.stickCollection = LineCollection([], colors='r')
        self.ax.add_collection(self.stickCollection)


    def _ok_clicked(self, event):
        plt.close(self.fig)

    def setXlabel(self, label):
        self.ax.set_xlabel(label)
    
    def setYlabel(self, label):
        self.ax.set_ylabel(label)

    def setXticks(self, on):
        self.ax.tick_params(which='both', bottom=on, labelbottom=on)

    def setYticks(self, on):
        self.ax.tick_params(which='both', left=on, labelleft=on)


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

    def get_slider_val(self, spec_name):
        return self.sliders[spec_name].val
    
    def get_check_enabled(self, spec_name):
        return self.checks[spec_name].get_status()[0]



    def update_slider(self, spec_name):
        slider = self.sliders[spec_name]
        textbox = self.textboxes[spec_name]

        if spec_name.split("_")[-1] in ["min", "max"]:
            spec_name = spec_name[:-4]
        digits = self._unpacked_specs[spec_name].get("digits", 2)

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
        digits = self._unpacked_specs[spec_name].get("digits", 2)
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

        sp = self._unpacked_specs[spec_name]
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

    def reset_sticks(self):
        self.stickCollection.set_segments([])

    def add_sticks(self, segments, plotset='static'):
        existing = self.stickCollection.get_segments()
        self.stickCollection.set_segments(existing + segments)

    def draw_sticks(self):
        self.ax.draw_artist(self.stickCollection)

    def plotXY(self, x, *y, plotset='static', color=None, **kwargs):
        self.plots.setdefault(plotset, [])

        if color is None:
            color = self.plotcolors.get(plotset, 'b')

        for yi in y:
            lineset = self.ax.plot(x, yi, color=color, **kwargs)
            self.plots[plotset].append(lineset)

    def draw_width_bracket(self, x_left, x_right, y, cap_height=0.1, plotset='static', color=None):
        self.plots.setdefault(plotset, [])

    def reset_plotsets(self, *plotsets):
        for plotset in plotsets:
            if plotset not in self.plots:
                return
            for drawer in self.plots[plotset]:
                if isinstance(drawer, list):
                    for d in drawer:
                        d.remove()
                else:
                    drawer.remove()
            self.plots[plotset] = []

    def update_plot(self, val=None):
        super().update_plot(val)
        self.fig.canvas.blit(self.ax.bbox)

    def main_loop(self):
        self.update_plot()
        plt.show()