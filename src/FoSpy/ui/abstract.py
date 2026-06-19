def _count_sliders(specs):
    total = 0
    for sp in specs.values():
        if sp["type"] == "scalar":
            total += 1
        elif sp["type"] == "range":
            total += 2
    return total

class SliderPlot:
    color1 = 'b'
    color2 = 'magenta'
    color3 = 'darkgreen'
    def __init__(self, specs={}, cfg={}, x_label=None, y_label=None, x_ticks=True, y_ticks=True):
        self.specs = specs
        self._unpacked_specs = {}
        self._unpack_specs()
        self.cfg = cfg
        self.sl_rows = _count_sliders(specs)
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
    from . import matplotlib, pyqtgraph
    from ..config import values as full_cfg
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

