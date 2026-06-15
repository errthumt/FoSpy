def _count_sliders(specs):
    total = 0
    for sp in specs.values():
        if sp["type"] == "scalar":
            total += 1
        elif sp["type"] == "range":
            total += 2
    return total

class SliderPlot:
    def __init__(self, specs={}, cfg={}):
        self.specs = specs
        self.cfg = cfg
        self.sl_rows = _count_sliders(specs)
        self.sliders = {}
        self.checks = {}
        self.textboxes = {}

    def update_plot(self, val=None):
        self.update_cfg()

    def update_cfg(self):
        for name, spec in self.specs.items():
            if spec["type"] == "scalar":
                enabled = self.get_check_enabled(name)
                self.cfg[name] = self.get_slider_val(name) if enabled else None

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
    
    def plotXY(self, x, *y):
        raise NotImplementedError("Override in UI subclass")
    
    def main_loop(self):
        raise NotImplementedError("Override in UI subclass")

