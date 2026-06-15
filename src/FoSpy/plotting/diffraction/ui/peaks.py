from ....ui.abstract import AssembleSlider

from ._specs import get_find_sliders


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
        from ..phase_match._utils import rows_to_2th
        from ..phase_match._utils import unpack_peaks

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
    PeakFinder = AssembleSlider(PeakFinderAbstract, ui=ui)

    return PeakFinder(exp_corrected, exp_index, cfg=cfg, **kwargs)