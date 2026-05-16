from pprint import pp

from parseTest import readTest, READ_PATH, WRITE_PATH, deep_diff

from FoSpy.blocks.synthesis import Synthesis

def constructTest():
    file_dict = readTest()
    #pp(file_dict)

    mySyn = Synthesis.fromFile(READ_PATH)

    # pp(mySyn._meta.__dict__)
    new_dict = mySyn.serialize()

    #pp(new_dict)
    # pp(mySyn.treatments[-1].program[0].__dict__)

    diffs = deep_diff(file_dict,new_dict)
    passed = diffs == []
    print(f"Checking file dict with serialized synthesis: {'passed' if passed else 'failed'}")

    if not passed:
        pp(diffs)

    mySyn.reaction.nominal_mass = "300.0"

    mySyn.save(WRITE_PATH)
    pass


constructTest()

pass