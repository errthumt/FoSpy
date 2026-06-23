from .abstract import SliderPlot as AbstractSlider, ControlPanel as AbstractControl
from ._utils import _get_digits

available = True
try:
    import pyqtgraph as pg
    from pyqtgraph.Qt import QtWidgets, QtCore

except ImportError as e:
    available = False
    import_e = e


TB_WIDTH = 60

CTRL_ROWS = 6
MIN_CTRL_WIDTH = 250
MAX_CTRL_HEIGHT = 65



def _separator():
    sep = QtWidgets.QFrame()
    sep.setFrameShape(QtWidgets.QFrame.VLine)
    sep.setFrameShadow(QtWidgets.QFrame.Sunken)
    sep.setLineWidth(2)   # thickness
    sep.setMidLineWidth(1)
    return sep

class ControlPanel(QtWidgets.QWidget, AbstractControl):
    def __init__(self, rows=CTRL_ROWS, parent=None):
        super().__init__(parent)
        AbstractControl.__init__(self, rows=rows)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.loner_grid = QtWidgets.QGridLayout()
        self.layout.addLayout(self.loner_grid)

        group_layout = QtWidgets.QHBoxLayout()
        self.group_select = QtWidgets.QVBoxLayout()
        self.group_panel = QtWidgets.QStackedWidget()
        group_layout.addLayout(self.group_select)
        group_layout.addWidget(_separator())
        group_layout.addWidget(self.group_panel)
        self.layout.addLayout(group_layout)

        self.group_buttons = QtWidgets.QButtonGroup()
        self.group_buttons.setExclusive(True)

        

    def addWidget(self, w):
        self.loner_grid.addWidget(w, *self.nextRowCol())

    def addGroup(self, label, rows=CTRL_ROWS):
        stack = ControlPanel(rows=rows, parent=self)

        btn = QtWidgets.QPushButton(label)
        btn.setCheckable(True)
        btn.clicked.connect(lambda _, label=label, stack=stack: self.group_panel.setCurrentWidget(stack))

        self.group_buttons.addButton(btn)
        self.group_select.addWidget(btn)

        self.group_panel.addWidget(stack)

        if self.group_panel.count() == 1:
            self.group_panel.setCurrentWidget(stack)
            btn.setChecked(True)

        return stack


# TODO: cleanup comments
# TODO: abstract _build_controls
class SliderPlot(AbstractSlider):
    def __init__(self, title="Interactive Plot", specs={}, cfg={}, x_label=None, y_label=None, x_ticks=True, y_ticks=True):
        if not available:
            raise ImportError(f"One or more required modules could not be imported. Exception:\n{import_e}")
        
        self.scheduled = []

        super().__init__(specs=specs, cfg=cfg, x_label=x_label, y_label=y_label, x_ticks=x_ticks, y_ticks=y_ticks)
        pg.setConfigOption('background', self.bg_color)
        pg.setConfigOption('foreground', self.fg_color)
        self.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        self.win = QtWidgets.QMainWindow()
        self.win.setWindowTitle(f"PyQtGraph | {title}")
        self.plot = pg.PlotWidget()

        for sch in self.scheduled:
            sch()
        

        self.sl_transforms = {}

        

        central = QtWidgets.QWidget()
        self.layout = QtWidgets.QHBoxLayout(central)
        self.win.setCentralWidget(central)

        self.layout.addWidget(self.plot, stretch=3)

        self.panel = ControlPanel(rows=CTRL_ROWS, parent=central)
        self.layout.addWidget(self.panel, stretch=1)
        self._build_controls()
        self.panel.group_select.addStretch(1)
        self.panel.layout.addStretch(1)

        ok_btn = QtWidgets.QPushButton("OK")
        ok_btn.clicked.connect(self._ok_clicked)
        self.panel.layout.addStretch(1)
        self.panel.layout.addWidget(ok_btn)

        self.sticks = []

        self._ok_pressed = False
        self._loop = QtCore.QEventLoop()

    def next_ctrl_row(self):
        if self._ctrl_row >= self._layout_rows-1:
            self._ctrl_col += 1
            self._ctrl_row = 0
        else:
            self._ctrl_row += 1

    def _ok_clicked(self):
        self._ok_pressed = True
        self.win.close()
        if self._loop.isRunning():
            self._loop.exit()

    def _build_controls(self, specs=None):
        super()._build_controls(specs=specs)
        
        self.panel.group_select.addStretch(1)
        self.panel.layout.addStretch(1)

    def _add_scalar(self, name, spec):
        box = QtWidgets.QGroupBox(spec["label"])
        box.setMinimumWidth(MIN_CTRL_WIDTH)
        box.setMaximumHeight(MAX_CTRL_HEIGHT)
        layout = QtWidgets.QHBoxLayout(box)

        # Checkbox
        check = QtWidgets.QCheckBox()
        check.setChecked(spec["default"] is not None)
        layout.addWidget(check)
        self.checks[name] = check

        # Find Slider Default
        if spec['default'] is not None:
            default = spec['default']
        elif name.endswith("_max"):
            default = spec['max']
        else:
            default = spec['min']

        digits = _get_digits(spec)
        step = 10**-digits
        sl_steps = int((spec["max"] - spec["min"]) / step)
        sl_transform = (
            lambda pos, spec=spec, sl_steps=sl_steps: spec["min"] + (pos * (spec["max"] - spec["min"]) / sl_steps),
            lambda val, spec=spec, sl_steps=sl_steps: int(round((val - spec["min"]) * sl_steps / (spec["max"] - spec["min"])))
        )
        self.sl_transforms[name] = sl_transform

        # Slider
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(sl_steps)
        slider.setValue(self._to_slider_pos(name, default))
        layout.addWidget(slider)
        self.sliders[name] = slider

        # Textbox
        tb = QtWidgets.QLineEdit(f"{default:.{_get_digits(spec)}f}")
        tb.setFixedWidth(TB_WIDTH)
        layout.addWidget(tb)
        self.textboxes[name] = tb

        # Wiring
        slider.valueChanged.connect(lambda _, n=name: self._slider_changed(n))
        check.stateChanged.connect(lambda _, n=name: self._check_changed(n))
        tb.editingFinished.connect(lambda n=name: self._textbox_changed(n))

        self.panel.addWidget(box)
        
    def _to_slider_pos(self, name, val):
        return self.sl_transforms[name][1](val)
    
    def _from_slider_pos(self, name, pos):
        return self.sl_transforms[name][0](pos)
    
    def setXlabel(self, label):
        if not hasattr(self, "plot"):
            self.scheduled.append(lambda label=label: self.setXlabel(label))
            return
        self.plot.setLabel("bottom", label)
    
    def setYlabel(self, label):
        if not hasattr(self, "plot"):
            self.scheduled.append(lambda label=label: self.setYlabel(label))
            return
        self.plot.setLabel("left", label)

    def setXticks(self, on):
        if not hasattr(self, "plot"):
            self.scheduled.append(lambda on=on: self.setXticks(on))
            return
        alpha = 1.0 if on else 0
        self.plot.getAxis("bottom").setStyle(tickAlpha=alpha, showValues=on)

    def setYticks(self, on):
        if not hasattr(self, "plot"):
            self.scheduled.append(lambda on=on: self.setYticks(on))
            return
        alpha = 1.0 if on else 0
        self.plot.getAxis("left").setStyle(tickAlpha=alpha, showValues=on)

    # Override abstract gets
    def get_slider_val(self, spec_name):
        slider = self.sliders[spec_name]

        return self._from_slider_pos(spec_name, slider.value())
    
    def get_check_enabled(self, spec_name):
        checked = self.checks[spec_name].isChecked()
        return checked

    def _slider_changed(self, spec_name):
        spec = self._spec_for(spec_name)
        val = self.get_slider_val(spec_name)
        digits = _get_digits(spec)

        self.textboxes[spec_name].setText(f"{val:.{digits}f}")
        self.update_plot()

    def _textbox_changed(self, spec_name):
        spec = self._spec_for(spec_name)
        tb = self.textboxes[spec_name]
        try:
            val = float(tb.text())
        except ValueError:
            val = self.get_slider_val(spec_name)

        # clamp to range:
        val = max(spec["min"], min(spec["max"], val))
        tb.setText(f"{val:.{_get_digits(spec)}f}")

        self.sliders[spec_name].setValue(self._to_slider_pos(spec_name, val))
        self.update_plot()

    def _check_changed(self, spec_name):
        self.update_plot()

    def _spec_for(self, spec_name):
        """Return the spec dict for scalar or range-min/max."""
        specs = self._unpacked_specs
        if spec_name.endswith("_min"):
            return {
                **specs[spec_name[:-4]],
                "default": specs[spec_name[:-4]]["default"][0]
            }
        if spec_name.endswith("_max"):
            return {
                **specs[spec_name[:-4]],
                "default": specs[spec_name[:-4]]["default"][1]
            }
        return specs[spec_name]
    
    def reset_sticks(self):
        for stick in self.sticks:
            self.plot.removeItem(stick)

        self.sticks.clear()
    
    def add_sticks(self, segments, plotset='static'):
        color = self.plotcolors.get(plotset, 'r')
        for (x0, y0), (x1, y1) in segments:
            stick = pg.PlotDataItem(
                x=[x0, x1],
                y=[y0, y1],
                pen=pg.mkPen(color,width=2)
            )
            self.sticks.append(stick)
    
    def draw_sticks(self):
        for item in self.sticks:
            self.plot.addItem(item)

    def draw_width_bracket(self, x_left, x_right, y, cap_height=0.1, plotset='static', color=None):
        self.plots.setdefault(plotset, [])
        if color is None:
            color = self.plotcolors.get(plotset, 'r')
        pen = pg.mkPen(color, width=1)


        hline = pg.PlotDataItem(
            x=[x_left, x_right],
            y=[y, y],
            pen=pen
        )

        l_cap, r_cap = [
            pg.PlotDataItem(
                x=[x, x],
                y=[y - cap_height, y + cap_height],
                pen=pen)
            for x in (x_left, x_right)
        ]

        for item in [hline, l_cap, r_cap]:
            self.plot.addItem(item)
            self.plots[plotset].append(item)

    def plotXY(self, x, *y, plotset='static', color=None, **kwargs):
        self.plots.setdefault(plotset, [])

        if color is None:
            color = self.plotcolors.get(plotset, 'b')

        for yi in y:
            item = self.plot.plot(x, yi, pen=pg.mkPen(color, width=2), **kwargs)
            self.plots[plotset].append(item)

    def reset_plotsets(self, *plotsets):
        for plotset in plotsets:
            if plotset not in self.plots:
                return
            
            for item in self.plots[plotset]:
                self.plot.removeItem(item)

            self.plots[plotset] = []
    
    def update_plot(self, val=None):
        super().update_plot(val)

    def main_loop(self):
        self.update_plot()

        self.win.show()
        self.app.processEvents()

        while not self._ok_pressed:
            self._loop.exec_()

        return None


    

