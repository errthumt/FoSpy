from pybaselines import Baseline

from FoSpy.plotting.diffraction.ui._specs import get_baseline_sliders

class BaselineFinderAbstract:
    def __init__(self, exp_int, exp_2th, cfg={}, **kwargs):
        self.exp_int = exp_int
        self.exp_2th = exp_2th
        specs = get_baseline_sliders(baseline_cfg=cfg, intensity_col=exp_int)
        super().__init__(specs=specs, cfg=cfg, **kwargs)

        self.plotXY(self.exp_2th, self.exp_int, plotset="static")

        self.fitter = Baseline()

    def update_baseline(self):
        self.update_cfg()

        args = self.cfg.copy()
        args["lam"] = 10**args["lam"]

        baseline, _ = self.fitter.arpls(self.exp_int,**args)

        self.baseline = baseline
        self.corrected = self.exp_int - baseline

        self.reset_plotset("results")
        self.plotXY(self.exp_2th, self.baseline, self.corrected, plotset="results")

    def update_plot(self, val=None):
        super().update_plot(val)
        self.update_baseline()

    def main_loop(self):
        super().main_loop()
        return self.baseline, self.corrected

    
        

