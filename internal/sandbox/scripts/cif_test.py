if __name__ == "__main__":
    import os
    import sys
    from pathlib import Path
    from FoSpy import Synthesis
    from FoSpy.plotting.diffraction.phase_match import PhaseMatcher
    from numpy import loadtxt
    from matplotlib import pyplot as plt
    from pprint import pp

    from FoSpy import cfg
    cfg.diffraction.default_engine = "pymatgen"

    ASSETS = Path(os.path.dirname(os.path.realpath(__file__))) / "../assets"
    FOS_PATH = ASSETS / "cif_test.fos"
    EXP_PATH = ASSETS / "As_experimental.xy"

    two_theta, intensity = loadtxt(EXP_PATH, unpack=True)

    my_syn = Synthesis.fromFile(FOS_PATH)

    my_syn.cifs[0].quick_pattern()

    cif_dict = {cif.file_name():cif for cif in my_syn.cifs}

    matcher = PhaseMatcher(two_theta, intensity, cif_dict)
    pp(matcher.frame)
    matcher.frame.plot()
    plt.show()



    pass