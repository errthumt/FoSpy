from parseTest import readTest, WRITE_PATH
from pprint import pp
from FoSpy import Synthesis

if __name__ == "__main__":
    full_dict = readTest()
    mySyn = Synthesis(full_dict)
    print(mySyn.metadata.internal_project_ID)
    print(mySyn.metadata.ext.internal_project_ID)
    print(mySyn.reaction.hijinks)


    serial = mySyn.serialize()
    mySyn.save(WRITE_PATH)
    pass

