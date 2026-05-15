from pprint import pp

from parseTest import readTest, READ_PATH, WRITE_PATH, deep_diff


from FoSpy.blocks.synthesis import Synthesis

def constructTest():
    file_dict = readTest()

    mySyn = Synthesis.fromFile(READ_PATH)

    new_dict = mySyn.serialize()

    # pp(new_dict)
    # pp(mySyn.treatments[-1].program[0].__dict__)

    passed = new_dict == file_dict
    print(f"Checking file dict with serialized synthesis: {'passed' if passed else 'failed'}")

    if not passed:
        pp(deep_diff(file_dict, new_dict))

    mySyn.reaction.nominal_mass = 300.0

    mySyn.save(WRITE_PATH)


constructTest()

pass