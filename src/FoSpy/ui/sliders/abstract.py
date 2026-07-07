from ._utils import _get_digits

def _count_sliders(specs):
    total = 0
    for sp in specs.values():
        if sp["type"] == "scalar":
            total += 1
        elif sp["type"] == "range":
            total += 2
    return total


CTRL_ROWS = 6

class ControlPanel:
    def __init__(self, rows=CTRL_ROWS):
        self._rowcol = self.row_col_iter()
        self._max_rows = rows

    def addWidget(self, w):
        pass

    def addGroup(self, label, rows=CTRL_ROWS):
        pass

    def row_col_iter(self):
        current_row = 0
        current_col = 0
        while True:
            if current_row >= self._max_rows-1:
                current_row = 0
                current_col += 1
            else:
                current_row += 1
            yield current_row, current_col
            

    def nextRowCol(self):
        return next(self._rowcol)

# TODO: handle bool specs
class SliderPlot:
    color1 = 'b'
    color2 = 'magenta'
    color3 = 'darkgreen'
    def __init__(self, specs={}, cfg={}, x_label=None, y_label=None, x_ticks=True, y_ticks=True):
        self.specs = specs
        self._unpacked_specs = {}
        self._unpack_specs()
        self.cfg = cfg
        self.sl_rows = _count_sliders(self._unpacked_specs)
        self.sliders = {}
        self.checks = {}
        self.textboxes = {}
        self.plots = {}
        self.plotcolors = {}

        self.bg_color = 'w'
        self.fg_color = 'k'

        if x_label is not None:
            self.setXlabel(x_label)
        if y_label is not None:
            self.setYlabel(y_label)

        self.setXticks(x_ticks)
        self.setYticks(y_ticks)

    def _unpack_specs(self, specs=None):
        specs = specs or self.specs

        for name, spec in specs.items():
            if spec["type"] == "group":
                self._unpack_specs(spec["specs"])
            else:
                self._unpacked_specs[name] = spec

    def update_plot(self, val=None):
        self.update_cfg()

    def update_cfg(self):
        for name, spec in self._unpacked_specs.items():
            if spec["type"] == "scalar":
                NoneVal = spec.get("None", None)
                enabled = self.get_check_enabled(name)
                self.cfg[name] = self.get_slider_val(name) if enabled else NoneVal

            elif spec["type"] == "range":
                lo_enabled = self.get_check_enabled(name + "_min")
                hi_enabled = self.get_check_enabled(name + "_max")

                lo = self.get_slider_val(name + "_min") if lo_enabled else None
                hi = self.get_slider_val(name + "_max") if hi_enabled else None

                self.cfg[name] = [lo, hi]

    def _add_group(self, label, specs, rows=CTRL_ROWS):
        # cache current panel
        panel = self.panel

        # reassign panel to nested group
        self.panel = panel.addGroup(label, rows=rows)

        # build controls in nested group
        self._build_controls(specs)

        # restore cached panel
        self.panel = panel

    def _add_range(self, name, spec):
        lo, hi = spec['default']

        specs = {
            name + "_min": {
                "label": "(min)",
                "min": spec["min"],
                "max": spec["max"],
                "default": lo,
                "digits": _get_digits(spec),
                "type": "scalar"
            },
            name + "_max": {
                "label": "(max)",
                "min": spec["min"],
                "max": spec["max"],
                "default": hi,
                "digits": _get_digits(spec),
                "type": "scalar"
            }
        }

        self._add_group(spec["label"], specs)

    def _build_controls(self, specs=None):
        specs = specs or self.specs
        widget_calls = {
            "scalar": lambda name, spec:
                self._add_scalar(name, spec),
            "range": lambda name, spec:
                self._add_range(name, spec),
            "group": lambda name, spec:
                self._add_group(spec["label"], spec["specs"])
        }
        def skip(name, spec):
            return None

        for name, spec in specs.items():
            widget_calls.get(spec["type"], skip)(name, spec)

        if specs == self.specs:
            self._finish_buttons()
    
    def _add_button(self, label, callback):
        # TODO: unit test
        raise NotImplementedError("Override in UI subclass")

    def _finish_buttons(self):
        # TODO: unit test
        for label, callback in (
            ("OK", self._ok_clicked),
            ("Reset to defaults", self.revert_cfg),
            ("Save as default", self.save_cfg)
        ):
            self._add_button(label, callback)

    def save_cfg(self):
        # TODO: unit test
        # TODO: abstract config save
        pass
    
    def revert_cfg(self):
        # TODO: unit test
        # TODO: abstract config revert
        pass

    def _ok_clicked(self):
        raise NotImplementedError("Override in UI subclass")

    def _add_scalar(self, name, spec):
        raise NotImplementedError("Override in UI subclass")

    def get_slider_val(self, spec_name):
        raise NotImplementedError("Override in UI subclass")
    
    def get_check_enabled(self, spec_name):
        raise NotImplementedError("Override in UI subclass")
    
    def reset_sticks(self):
        raise NotImplementedError("Override in UI subclass")
    
    def add_sticks(self, segments):
        raise NotImplementedError("Override in UI subclass")
    
    def draw_sticks(self):
        raise NotImplementedError("Override in UI subclass")
    
    def plotXY(self, x, *y, plotset='static',**kwargs):
        raise NotImplementedError("Override in UI subclass")
    
    def reset_plotsets(self, *plotsets):
        raise NotImplementedError("Override in UI subclass")
    
    def main_loop(self):
        raise NotImplementedError("Override in UI subclass")
    
    def setXlabel(self, label):
        raise NotImplementedError("Override in UI subclass")
    
    def setYlabel(self, label):
        raise NotImplementedError("Override in UI subclass")

    def setXticks(self, on):
        raise NotImplementedError("Override in UI subclass")

    def setYticks(self, on):
        raise NotImplementedError("Override in UI subclass")


def AssembleSlider(subcls, ui=None):
    from .. import matplotlib, pyqtgraph
    from ...config import values as full_cfg
    ui_opts = {
        'matplotlib': matplotlib,
        'pyqtgraph': pyqtgraph
    }

    if ui is None:
        ui = full_cfg.get('ui.default')

    plot_module = ui_opts.get(ui, matplotlib)

    if not plot_module.available:
        plot_module = matplotlib

    class SliderPlot(subcls, plot_module.SliderPlot):
        pass


    return SliderPlot

