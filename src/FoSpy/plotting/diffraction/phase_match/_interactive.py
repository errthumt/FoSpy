from ....config import values as cfg
import math

def check_for_interactive(interactive, kw):
    if isinstance(interactive, bool):
        return interactive
    elif isinstance(interactive, str):
        return interactive == kw
    elif isinstance(interactive, list):
        return kw in interactive

def floor_to(x, digits):
    return math.floor(x * 10**digits) / 10**digits

def ceil_to(x, digits):
    return math.ceil(x * 10**digits) / 10**digits

def round_spec(x, digits, key=None):
    if isinstance(x, list or tuple):
        return [round_spec(xi, digits) for xi in x]
    elif key == "min":
        return floor_to(x, digits)
    elif key == "max":
        return ceil_to(x, digits)
    else:
        return round(x, digits) if x is not None else None

def get_find_sliders(find_cfg, intensity_col):
    sliders = {
        "height": {
            "type": "range",
            "label": "Peak Height",
            "min": 0,
            "max": max(intensity_col),
        },
        "threshold": {
            "type": "range",
            "label": "Threshold",
            "min": 0,
            "max": 1
        },
        "distance": {
            "type": "scalar",
            "label": "Min Distance (samples)",
            "min": 1,
            "max": len(intensity_col),
            "int": True
        },
        "prominence": {
            "type": "range",
            "label": "Prominence",
            "min": 0,
            "max": max(intensity_col),
        },
        "width": {
            "type": "range",
            "label": "Width (samples)",
            "min": 0,
            "max": len(intensity_col),
            "int": True
        },
        "wlen": {
            "type": "scalar",
            "label": "Window Length",
            "min": 2,
            "max": len(intensity_col),
            "int": True,
        },
        "rel_height": {
            "type": "scalar",
            "label": "Relative Height",
            "min": 0,
            "max": 1,
        },
        "plateau_size": {
            "type": "range",
            "label": "Plateau Size",
            "min": 0,
            "max": len(intensity_col),
            "int": True
        }
    }
    digits_default = cfg.get("slider_digits.default")
    digit_cfg = cfg.get("slider_digits.find_peaks")
    for name, spec in sliders.items():
        if spec.get("int", False):
            digits = 0
        else:
            digits = digit_cfg.get(name, None) or digits_default
        spec["digits"] = digits

        spec["default"] = find_cfg.get(name)

        for key in ["min", "max", "default"]:
            spec[key] = round_spec(spec[key], digits, key)
        
    return sliders


class PeakFinderAbstract:
    def __init__(self, exp_corrected, exp_index, cfg={}, **kwargs):
        specs = get_find_sliders(cfg, exp_corrected)
        self.exp_corrected = exp_corrected
        self.exp_index = exp_index
        super().__init__(specs=specs, cfg=cfg, **kwargs)

        from matplotlib.collections import LineCollection

        self.sticks = []

        self.peaks, self.widths = None, None

        self.plotXY(self.exp_index, self.exp_corrected)

    def update_sticks(self):
        if not hasattr(self, 'exp_corrected') and hasattr(self, 'exp_index'):
            return
        from ._utils import rows_to_2th
        from .match import unpack_peaks

        self.peaks, self.widths = unpack_peaks(self.exp_corrected,
        "widths", **self.cfg)

        peaks_list = [int(x) for x in self.peaks]
        intensity_list = [self.exp_corrected[x] for x in peaks_list]
        peaks_2th = rows_to_2th(self.exp_index, peaks_list)

        segments = [ [(x, 0), (x, y)] for x, y in zip(peaks_2th, intensity_list)]
        self.reset_sticks()
        self.add_sticks(segments)
        self.draw_sticks()
        
    
    def update_plot(self, val=None):
        super().update_plot(val)
        self.update_sticks()

    def main_loop(self):
        super().main_loop()
        return self.peaks, self.widths
    

def PeakFinder(exp_corrected, exp_index, cfg={}, ui=None, **kwargs):
    from ....ui.matplotlib import SliderPlot as matSliderPlot
    from ....ui.pyqtgraph import SliderPlot as pgSliderPlot
    from ....config import values as full_cfg
    ui_opts = {
        'matplotlib': matSliderPlot,
        'pyqtgraph': pgSliderPlot
    }

    if ui is None:
        ui = full_cfg.get('ui.default')

    plot_cls = ui_opts.get(ui, matSliderPlot)

    class PeakFinder(PeakFinderAbstract, plot_cls):
        pass

    return PeakFinder(exp_corrected, exp_index, cfg=cfg, **kwargs)
