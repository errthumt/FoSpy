from FoSpy.blocks.synthesis import Synthesis



if __name__ == "__main__":
    mySyn = Synthesis.fromFile("tests/test_fos/start_synthesis.fos")

    clathrate = mySyn.cifs[0]

    clathrate.quick_pattern(subprocess=True)
    print("I'm still running")
    pass