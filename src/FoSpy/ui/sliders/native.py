from ..available import validate_ui, UINotAvailable
import tkinter as tk
try:
    validate_ui("native")
    from .abstract import SliderPlot as AbstractSlider, ControlPanel as AbstractControl, CTRL_ROWS
    from matplotlib.collections import LineCollection
    from ._utils import _get_digits
    available = True
    import_e = None
except Exception as e:
    # fallbacks to prevent crash if UI not available
    AbstractSlider = object
    AbstractControl = object
    CTRL_ROWS = 0

    available = False

    if isinstance(e, UINotAvailable):
        import_e = e
    else:
        import_e = ImportError("Native UI not available for unexpected exception")
        import_e.__cause__ = e

def _import_gate():
    global available, import_e
    if not available:
        raise import_e


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
        _import_gate()

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
        
        _import_gate()

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