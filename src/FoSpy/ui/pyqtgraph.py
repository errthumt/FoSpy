from .abstract import SliderPlot as AbstractSlider
from ..config import values as full_cfg

available = True
try:
    import pyqtgraph as pg
    from pyqtgraph.Qt import QtWidgets, QtCore

except ImportError as e:
    available = False
    import_e = e

TB_WIDTH = 60
DEF_DIGITS = full_cfg.get("slider_digits.default", 2)

def _get_digits(spec):
    return spec.get("digits", DEF_DIGITS)

class SliderPlot(AbstractSlider):
    def __init__(self, title="Interactive Plot", specs={}, cfg={}):
        if not available:
            raise ImportError(f"One or more required modules could not be imported. Exception:\n{import_e}")


        super().__init__(specs=specs, cfg=cfg)

        self.sl_transforms = {}

        self.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

        self.win = QtWidgets.QMainWindow()
        self.win.setWindowTitle(f"PyQtGraph | {title}")

        central = QtWidgets.QWidget()
        self.layout = QtWidgets.QHBoxLayout(central)
        self.win.setCentralWidget(central)

        self.plot = pg.PlotWidget()
        self.layout.addWidget(self.plot, stretch=3)

        self.ctrl_panel = QtWidgets.QWidget()
        self.ctrl_layout = QtWidgets.QVBoxLayout(self.ctrl_panel)
        self.layout.addWidget(self.ctrl_panel, stretch=1)

        self._build_controls()

        self.sticks = []

        self._ok_pressed = False
        self._loop = QtCore.QEventLoop()

    def _ok_clicked(self):
        self._ok_pressed = True
        self.win.close()
        if self._loop.isRunning():
            self._loop.exit()

        

    def _build_controls(self):
        for name, spec in self.specs.items():
            if spec["type"] == "scalar":
                self._add_scalar(name, spec)

            elif spec["type"] == "range":
                self._add_range(name, spec)

        ok_btn = QtWidgets.QPushButton("OK")
        ok_btn.clicked.connect(self._ok_clicked)
        self.ctrl_layout.addWidget(ok_btn)

        self.ctrl_layout.addStretch()

    def _add_scalar(self, name, spec):
        box = QtWidgets.QGroupBox(spec["label"])
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

        self.ctrl_layout.addWidget(box)

    def _add_range(self, name, spec):
        lo, hi = spec['default']

        self._add_scalar(name + "_min",
                         spec={"label": spec["label"] + " (min)",
                               "min": spec["min"],
                               "max": spec["max"],
                               "default": lo,
                               "digits": _get_digits(spec),
                               "type": "scalar"})
        
        self._add_scalar(name + "_max",
                         spec={"label": spec["label"] + " (max)",
                               "min": spec["min"],
                               "max": spec["max"],
                               "default": hi,
                               "digits": _get_digits(spec),
                               "type": "scalar"})
        
    def _to_slider_pos(self, name, val):
        return self.sl_transforms[name][1](val)
    
    def _from_slider_pos(self, name, pos):
        return self.sl_transforms[name][0](pos)
    
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
        if spec_name.endswith("_min"):
            return {
                **self.specs[spec_name[:-4]],
                "default": self.specs[spec_name[:-4]]["default"][0]
            }
        if spec_name.endswith("_max"):
            return {
                **self.specs[spec_name[:-4]],
                "default": self.specs[spec_name[:-4]]["default"][1]
            }
        return self.specs[spec_name]
    
    def reset_sticks(self):
        for stick in self.sticks:
            self.plot.removeItem(stick)

        self.sticks.clear()
    
    def add_sticks(self, segments):
        for (x0, y0), (x1, y1) in segments:
            stick = pg.PlotDataItem(
                x=[x0, x1],
                y=[y0, y1],
                pen=pg.mkPen('r',width=2)
            )
            self.sticks.append(stick)
    
    def draw_sticks(self):
        for item in self.sticks:
            self.plot.addItem(item)

    def plotXY(self, x, *y, plotset='static', pen=pg.mkPen('b', width=2), **kwargs):
        self.plots.setdefault(plotset, [])

        for yi in y:
            item = self.plot.plot(x, yi, pen=pen, **kwargs)
            self.plots[plotset].append(item)

    def reset_plotset(self, plotset='static'):
        if plotset not in self.plots:
            return
        
        for item in self.plots[plotset]:
            self.plot.removeItem(item)

        self.plots[plotset] = []
    
    def update_plot(self, val=None):
        super().update_plot(val)

        txt = "\n".join(f"{k}: {v}" for k, v in self.cfg.items())
        self.plot.addItem(pg.TextItem(txt, anchor=(0,0)))

    def main_loop(self):
        self.update_plot()

        self.win.show()
        self.app.processEvents()

        while not self._ok_pressed:
            self._loop.exec_()

        return None


    

