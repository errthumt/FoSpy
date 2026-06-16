from pybaselines import Baseline

from ._specs import get_baseline_sliders
from ....ui.abstract import AssembleSlider
from ..phase_match._utils import convert_baseline_cfg

class BaselineFinderAbstract:
    def __init__(self, exp_int, exp_2th, cfg={}, **kwargs):
        self.exp_int = exp_int
        self.exp_2th = exp_2th
        self.offset = max(exp_int)
        specs = get_baseline_sliders(baseline_cfg=cfg)
        super().__init__(specs=specs, cfg=cfg, **kwargs)

        self.plotXY(self.exp_2th, self.exp_int+self.offset, plotset="static", color='b')

        self.fitter = Baseline()

    def update_baseline(self):
        self.update_cfg()

        args = convert_baseline_cfg(self.cfg)

        baseline, _ = self.fitter.arpls(self.exp_int,**args)

        self.baseline = baseline
        self.corrected = self.exp_int - baseline

        self.reset_plotset("results")
        self.plotXY(self.exp_2th, self.baseline+self.offset, color='r', plotset="results")
        self.plotXY(self.exp_2th, self.corrected, color='g', plotset="results")

    def update_plot(self, val=None):
        super().update_plot(val)
        self.update_baseline()

    def main_loop(self):
        super().main_loop()
        return self.baseline, self.corrected
    
def BaselineFinder(exp_int, exp_2th, ui=None, cfg={}, **kwargs):
    BaselineFinder = AssembleSlider(BaselineFinderAbstract, ui=ui)

    return BaselineFinder(exp_int, exp_2th, cfg=cfg, **kwargs)

    
        

