from parseTest import readTest, WRITE_PATH
from pprint import pp
from FoSpy import Synthesis, FileBlock

from FoSpy._debug import all_debugs_on
all_debugs_on(soundoff=False)

if __name__ == "__main__":
    full_dict = readTest()
    mySyn = Synthesis(full_dict)
    print(mySyn.metadata.internal_project_ID)
    print(mySyn.metadata.ext.internal_project_ID)
    #print(mySyn.reaction.hijinks)
    #pp(mySyn.cif.serialize.__doc__)
    mySyn.add_calc_routine("materials[1].add_MW")
    print(mySyn.materials.add_all_MW.__doc__)
    serial = mySyn.serialize()
    mySyn.save(WRITE_PATH)
    pass

