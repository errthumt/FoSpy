if __name__ == "__main__":
    import os
    from pathlib import Path
    from FoSpy import Synthesis
    from FoSpy.plotting.diffraction.phase_match import PhaseMatcher
    from numpy import loadtxt
    from matplotlib import pyplot as plt
    from FoSpy.config import values as cfg
    from FoSpy.plotting.diffraction.phase_match.match import _debug
    _debug.on = True


    X_LABEL = cfg.diffraction.x_label

    from FoSpy import cfg
    cfg.diffraction.default_engine = "pymatgen"

    ASSETS = Path(os.path.dirname(os.path.realpath(__file__))) / "../assets"
    FOS_PATH = ASSETS / "cif_test.fos"
    EXP_PATH = ASSETS / "As_experimental.xy"

    two_theta, intensity = loadtxt(EXP_PATH, unpack=True)
    intensity = intensity / max(intensity)

    my_syn = Synthesis.fromFile(FOS_PATH)

    # my_syn.cifs[0].quick_pattern()

    cif_dict = {cif.file_name():cif for cif in my_syn.cifs}

    matcher = PhaseMatcher(two_theta, intensity, cif_dict)
    # for name, frame in matcher.frames.items():
    #     fig, ax = plt.subplots()
    #     frame.plot(title=name, ax=ax)

    fig, ax = plt.subplots()

    # matcher.find_baseline(interactive=True)
    matcher.find_peaks(interactive='find')

    #matcher.frames['exp'].plot()

    plt.show()
    pass