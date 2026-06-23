from ....ui.abstract import AssembleSlider
from ....config import values as full_cfg

from ._specs import get_find_sliders

X_LABEL = full_cfg.diffraction.x_label

class PeakFinderAbstract:
    def __init__(self, exp_corrected, exp_index, cfg={}, **kwargs):
        specs = get_find_sliders(cfg, exp_corrected)
        self.exp_corrected = exp_corrected
        self.exp_index = exp_index
        self.max_h = max(exp_corrected)
        super().__init__(specs=specs, cfg=cfg, x_label=X_LABEL, y_ticks=False, y_label="Intensity", **kwargs)

        self.plotcolors = {
            'static': self.color1,
            'peaks': self.color2,
            'widths': self.color3
        }

        self.sticks = []

        self.peaks, self.widths = None, None

        self.plotXY(self.exp_index, self.exp_corrected)

    def update_peaks(self):
        if not hasattr(self, 'exp_corrected') and hasattr(self, 'exp_index'):
            return
        from ..phase_match._utils import rows_to_2th
        from ..phase_match._utils import unpack_peaks

        self.peaks, self.widths, w_heights  = unpack_peaks(self.exp_corrected,
        "widths", "width_heights", **self.cfg)

        peaks_list = [int(x) for x in self.peaks]
        intensity_list = [self.exp_corrected[x] for x in peaks_list]
        peaks_2th = rows_to_2th(self.exp_index, peaks_list)

        segments = [ [(x, 0), (x, y)] for x, y in zip(peaks_2th, intensity_list)]
        self.reset_sticks()
        self.add_sticks(segments, plotset='peaks')
        self.draw_sticks()

        self.update_widths(self.peaks, self.widths, w_heights)
    
    def update_widths(self, peaks, widths, w_heights):
        from ..phase_match._utils import rows_to_2th

        def clamp(x, minimum, maximum):
            return max(minimum, min(x, maximum))

        if len(peaks)==0:
            return
        brackets_x = [
            [clamp(round(x),0,len(self.exp_index)-1) 
             for x in [peak+width/2, peak-width/2]] 
             for peak, width in zip(peaks, widths)
        ]

        brackets_2th = rows_to_2th(self.exp_index, brackets_x)

        y_base = -0.02 * self.max_h
        cap_height = -y_base/4
        self.reset_plotsets('widths')
        buffer = 2 * max(tth_right-tth_left for (tth_left, tth_right) in brackets_2th)



        for (tth_left, tth_right), y in zip(brackets_2th, w_heights):
            self.draw_width_bracket(tth_left-buffer, tth_right+buffer, y, cap_height=cap_height, plotset='widths')
            self.draw_width_bracket(tth_left, tth_right, y_base, cap_height=cap_height, plotset='widths')



    def update_plot(self, val=None):
        super().update_plot(val)
        self.update_peaks()

    def main_loop(self):
        super().main_loop()
        return self.peaks, self.widths


def PeakFinder(exp_corrected, exp_index, cfg={}, ui=None, **kwargs):
    PeakFinder = AssembleSlider(PeakFinderAbstract, ui=ui)

    return PeakFinder(exp_corrected, exp_index, cfg=cfg, **kwargs)