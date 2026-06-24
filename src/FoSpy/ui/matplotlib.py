from .abstract import SliderPlot as AbstractSlider, ControlPanel as AbstractControl, CTRL_ROWS

from matplotlib.collections import LineCollection
import tkinter as tk
from ._utils import _get_digits

available = True

# -------------------------------
# Layout constants for UI elements
# -------------------------------
# LEFT_MARGIN = 0.05
# RIGHT_MARGIN = 0.02

START_Y = 0.2
PANEL_START = 0.70
# PANEL_W = 1.0 - PANEL_START
PADDING = 0.02
CHECK_X      = PANEL_START+PADDING
CHECK_W      = 0.06
SLIDER_X     = CHECK_X + CHECK_W + PADDING
SLIDER_W     = 1.0 - SLIDER_X - PADDING
# LABEL_LSHIFT = (CHECK_W + 2*PADDING) / SLIDER_W
# ROW_H        = 0.03

# ROW_SPACING  = 0.05

# OK_BTN_W     = 0.20
# OK_BTN_H     = START_Y / 2

def _get_label_offset(slider_width):
    offset = 2*PADDING + CHECK_W

    offset = offset / slider_width
    return offset

def _hseparator(parent=None):
    frame = tk.Frame(parent, height=2, bg="#888")
    frame.pack(fill='x', side='top', padx=4, pady=4)
    return frame

def _vseparator(parent=None):
    frame = tk.Frame(parent, width=2, height=1, bg="#888")
    frame.pack(fill='y',side='left', padx=4, pady=4)
    return frame

class ControlPanel(tk.Frame,AbstractControl):
    def __init__(self, rows=CTRL_ROWS, parent=None, add_buttons=False):
        tk.Frame.__init__(self, parent)
        AbstractControl.__init__(self, rows=rows)

        self._seps = []

        self.loner_grid = tk.Frame(self)
        self.loner_grid.pack(side='top', fill='x')
        self._seps.append(_hseparator(self))

        if add_buttons:
            self.button_panel = tk.Frame(self)
            self.button_panel.pack(side='bottom', fill='y', anchor='nw', expand=True)

        self.group_select = tk.Frame(self)
        self.group_select.pack(side='left',anchor='n', fill='none')

        self.groups = {}

    @classmethod
    def withButtons(cls, *args, **kwargs):
        kwargs.setdefault('add_buttons', True)
        obj = cls(*args, **kwargs)
        return obj, obj.button_panel

    def addWidget(self, w):
        r,c = self.nextRowCol()
        w.grid(in_=self.loner_grid, row=r, column=c, sticky='w')

        

    def addGroup(self, label, rows=CTRL_ROWS):
        if len(self.groups) == 0:
            self._seps.append(_vseparator(self))

            self.group_panel = tk.Frame(self)
            self.group_panel.pack(side='left', fill= 'x', anchor='n', expand=True)

        btn = tk.Button(self.group_select, text=label)
        btn.pack(fill='x')

        frame = ControlPanel(parent=self.group_panel, rows=rows)

        self.groups[frame] = btn

        btn.config(command=lambda f=frame: self._show_group(f))

        self._show_group(frame)

        return frame

    def _show_group(self, frame):
        for g, b in self.groups.items():
            g.pack_forget()

            # unselect button
            b.config(relief='raised')

        frame.pack(fill='x', expand=True)
        self.groups[frame].config(relief='sunken')



class SliderPlot(AbstractSlider):
    def __init__(self, figsize=(10,6), title="Interactive Plot", specs={}, cfg={}, x_label=None, y_label=None, x_ticks=True, y_ticks=True):
        
        # try:
        #     matplotlib.use(backend)
        # except Exception as e:
        #     from warnings import warn
        #     warn(f"Could not set matplotlib backend to {backend}. Using system default. "
        #          f"Exception:\n{e}", RuntimeWarning)

        # self.fig, self.ax = plt.subplots(figsize=figsize)

        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure

        self.root = tk.Tk()
        self.fig = Figure(figsize=figsize)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

        self.panel, self._button_column = ControlPanel.withButtons(parent=self.root)
        self.panel.pack(side="right", fill="y")

        self._buttons = []

        super().__init__(specs=specs, cfg=cfg, x_label=x_label, y_label=y_label, x_ticks=x_ticks, y_ticks=y_ticks)

        self._build_controls()

        self._return = tk.BooleanVar(value=False)

        # self.ok_btn = tk.Button(self.panel, text="OK", command=self._ok_clicked)
        # self.ok_btn.pack(side="bottom", fill="x")



        # self.sl_rows = len(specs)

        # #self.labels = {sp['label']: k for k, sp in specs.items()}

        # self.row_height = 1.0 / self.sl_rows

        # self.ax.set_title(title)

        # self.panel_ax = self.fig.add_axes([PANEL_START, START_Y, PANEL_W, 1-START_Y])
        # self.panel_ax.set_title("Parameters", fontsize=16)
        # self.panel_ax.set_axis_off()
        # self.panel_width = self.panel_ax.get_window_extent().width
        # self.pilot_slider = Slider(self.panel_ax.inset_axes([0, 0, 1, 1]), "", 0, 1, valinit=0, dragging=False)
        # self.max_label_width = 0.0

        # self.ypos = 0

        # # TODO: better group organization
        # # temporary: unpack groups
        # unpacked = {}
        # for name, spec in specs.items():
        #     if spec["type"] == "group":
        #         grp_label = spec["label"]
        #         grp_name = name
        #         for nm, spc in spec["specs"].items():
        #             spc["label"] = f"({grp_label}) {spc['label']}"
        #             unpacked[f"{grp_name}_{nm}"] = spc
        #     else:
        #         unpacked[name] = spec

        # specs = unpacked

        # for name, spec in specs.items():
        #     if spec["type"] == "scalar":
        #         self.add_slider(name)
        #     elif spec["type"] == "range":
        #         self.add_slider(name, range_type="min")
        #         self.add_slider(name, range_type="max")

        # self.pilot_slider.disconnect_events()
        # for vis in (
        #     self.pilot_slider.ax,
        #     self.pilot_slider.label,
        #     self.pilot_slider.valtext,
        #     self.pilot_slider.poly
        # ):
        #     vis.set_visible(False)

        # fig_width = self.fig.get_window_extent().width
        # label_width = self.max_label_width / fig_width
        # label_width += (3*PADDING + CHECK_W) * PANEL_W
        # plt.subplots_adjust(left=LEFT_MARGIN, right=PANEL_START-label_width)

        # ok_center = (1.0 + PANEL_START - label_width) / 2.0
        # ok_start_x = ok_center - OK_BTN_W/2.0
        # ok_start_y = START_Y / 4.0
        # ok_ax = self.fig.add_axes([ok_start_x, ok_start_y, OK_BTN_W, OK_BTN_H])
        # ok_ax.set_zorder(1000)
        # self.ok_btn = Button(ok_ax, 'OK')
        # self.ok_btn.on_clicked(self._ok_clicked)

        self.stickCollection = LineCollection([], colors='r')
        self.ax.add_collection(self.stickCollection)

    def _add_scalar(self, name, spec):
        frame = tk.LabelFrame(self.panel, text=spec["label"])

        none_val = spec["max"] if name.endswith("_max") else spec["min"]
        default = spec["default"] or spec.get("None", none_val)
        digits = _get_digits(spec)

        var_enabled = tk.BooleanVar(value=default is not None)
        var_slider = tk.DoubleVar(value=default)
        var_text = tk.StringVar(value=f"{default:.{digits}f}")

        #checkbox
        chk = tk.Checkbutton(frame, variable=var_enabled)
        chk.pack(side='left')

        #slider
        slider = tk.Scale(frame, from_=spec["min"], to=spec["max"], orient='horizontal', variable=var_slider, resolution=10**-digits)
        slider.pack(side="left", fill="x", expand=True)

        # textbox
        entry = tk.Entry(frame, textvariable=var_text, width=8)
        entry.pack(side="left")

        self.checks[name] = var_enabled
        self.sliders[name] = var_slider
        self.textboxes[name] = var_text

        var_slider.trace_add("write", lambda *_ ,n=name, d=digits: self.slider_changed(n, d))
        var_text.trace_add("write", lambda *_ ,n=name, d=digits, m=spec["min"], M=spec["max"]: self.textbox_changed(n, d, m, M))
        var_enabled.trace_add("write", lambda *_ ,n=name: self.toggle_slider(n))

        self.panel.addWidget(frame)

    def slider_changed(self, name, digits):
        val = self.sliders[name].get()

        text = self.textboxes[name]
        text.set(f"{val:.{digits}f}")

        self.update_plot()

    def textbox_changed(self, name, digits, min_, max_):
        tb = self.textboxes[name]
        slider = self.sliders[name]

        txt = tb.get()
        try:
            val = float(txt)
        except ValueError:
            # restore slider value
            sl_val = slider.get()
            tb.set(f"{sl_val:.{digits}f}")
            return
        
        # clamp
        val = max(min_, min(max_, val))

        slider.set(val)
        tb.set(f"{val:.{digits}f}")

        self.update_plot()

    def _add_button(self, label, callback):
        # TODO: unit test
        btn = tk.Button(self._button_column, text=label, command=callback)
        btn.pack(side='top', anchor='w', pady=2)

        self._buttons.append(btn)

    def _finish_buttons(self):
        # TODO: unit test

        super()._finish_buttons()


    def _ok_clicked(self):
        self._return.set(True)
        self.root.destroy()

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
        tb = self.textboxes[spec_name]

        sl.config(state="disabled")
        tb.config(state="disabled")

        self.update_plot()


    def enable_slider(self, spec_name):
        sl = self.sliders[spec_name]
        tb = self.textboxes[spec_name]

        sl.config(state="normal")
        tb.config(state="normal")

        self.update_plot()

    
    def toggle_slider(self, spec_name):
        if self.get_check_enabled(spec_name):
            self.enable_slider(spec_name)
        else:
            self.disable_slider(spec_name)

    def get_slider_val(self, spec_name):
        return self.sliders[spec_name].get()
    
    def get_check_enabled(self, spec_name):
        return self.checks[spec_name].get()

    # def update_slider(self, spec_name):
    #     slider = self.sliders[spec_name]
    #     textbox = self.textboxes[spec_name]

    #     if spec_name.split("_")[-1] in ["min", "max"]:
    #         spec_name = spec_name[:-4]
    #     digits = self._unpacked_specs[spec_name].get("digits", 2)

    #     def update(val, slider=slider, textbox=textbox, digits=digits):
    #         try:
    #             if not slider.active:
    #                 raise ValueError
    #             slider.set_val(float(val))
    #             self.update_plot()
    #         except ValueError:
    #             textbox.set_val(f"{slider.val:.{digits}f}")

    #     return update
    
    # def update_textbox(self, spec_name):
    #     textbox = self.textboxes[spec_name]
    #     slider = self.sliders[spec_name]
    #     if spec_name.split("_")[-1] in ["min", "max"]:
    #         spec_name = spec_name[:-4]
    #     digits = self._unpacked_specs[spec_name].get("digits", 2)
    #     def update(val, slider=slider, textbox=textbox, digits=digits):
    #         if not slider.active:
    #             slider.set_val(float(textbox.val))
    #         else:
    #             textbox.set_val(f"{slider.val:.{digits}f}")
    #             self.update_plot()
    #     return update

    # def add_slider(self, spec_name, range_type=None):
    #     from matplotlib.widgets import Slider, CheckButtons, TextBox
    #     from mpl_toolkits.axes_grid1.inset_locator import inset_axes

    #     sp = self._unpacked_specs[spec_name]
    #     label = sp['label']

    #     if range_type is None:
    #         default = sp['default']
    #     elif range_type == 'min':
    #         default = sp['default'][0]
    #         spec_name = spec_name + "_min"
    #         label = label + " (min)"
    #     elif range_type == 'max':
    #         default = sp['default'][1]
    #         spec_name = spec_name + "_max"
    #         label = label + " (max)"

    #     enabled = default is not None
    #     check_ax = self.panel_ax.inset_axes([-CHECK_W-PADDING, self.ypos, CHECK_W, self.row_height/2])
    #     check = CheckButtons(check_ax, [spec_name], [enabled],label_props={'fontsize':[14]},)
    #     check.labels[0].set_visible(False)
    #     self.checks[spec_name] = check

    #     digits = sp.get('digits', 2)
    #     self.pilot_slider.valtext.set_text(f"{sp['max']:.{digits}f}")
    #     text_width = self.pilot_slider.valtext.get_window_extent().width
    #     text_width = text_width / self.panel_width
    #     tb_width = text_width + PADDING

    #     if default is None:
    #         default = sp['max'] if range_type=='max' else sp['min']

    #     sl_width = 1-tb_width-2*PADDING
    #     ax_sl = self.panel_ax.inset_axes([0, self.ypos, sl_width, self.row_height/2])
    #     slider = Slider(ax_sl,label, sp['min'], sp['max'], valinit=default, valstep=(10**-digits), dragging=True)
    #     slider.valtext.set_visible(False)
    #     self.sliders[spec_name] = slider

    #     label_width = slider.label.get_window_extent().width
    #     if label_width > self.max_label_width:
    #         self.max_label_width = label_width

    #     label_offset = _get_label_offset(sl_width)
    #     slider.label.set_position((-label_offset, 0.5))

    #     ax_text = self.panel_ax.inset_axes([1.0-tb_width-PADDING, self.ypos, tb_width, self.row_height/2])
    #     textbox = TextBox(ax_text, "", initial=f"{slider.val:.{sp.get('digits', 2)}f}")
    #     self.textboxes[spec_name] = textbox

    #     slider.on_changed(self.update_textbox(spec_name))
    #     textbox.on_submit(self.update_slider(spec_name))
    #     check.on_clicked(self.toggle_slider)

    #     slider.active = enabled
        

    #     self.ypos += self.row_height

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

    def draw_width_bracket(self, x_left, x_right, y, cap_height=0.1,
                        plotset='static', color=None):

        # Ensure plotset exists
        self.plots.setdefault(plotset, [])

        # Choose color
        if color is None:
            color = self.plotcolors.get(plotset, 'r')

        # Horizontal line
        hline, = self.ax.plot(
            [x_left, x_right],
            [y, y],
            color=color,
            linewidth=1
        )

        # Left cap
        lcap, = self.ax.plot(
            [x_left, x_left],
            [y - cap_height, y + cap_height],
            color=color,
            linewidth=1
        )

        # Right cap
        rcap, = self.ax.plot(
            [x_right, x_right],
            [y - cap_height, y + cap_height],
            color=color,
            linewidth=1
        )

        # Store all three artists in the plotset
        for item in (hline, lcap, rcap):
            self.plots[plotset].append(item)

        # Redraw
        self.canvas.draw_idle()


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
        self.canvas.draw_idle()

    def main_loop(self):
        self.update_plot()
        self.root.wait_variable(self._return)