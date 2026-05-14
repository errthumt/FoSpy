from . import SingleBlock, ListBlock

class Treatment(SingleBlock):
    # Maps type strings to subclass constructors.
    # Populated after each subclass definition.
    dispatch = {}

    @classmethod
    def from_blockList(cls, blockDict):
        t = blockDict.get("type")
        subclass = cls.dispatch.get(t,cls)
        return subclass(blockDict)

    def __init__(self, blockDict):
        super().__init__(blockDict)

class Annealing(Treatment):
    def __init__(self, blockDict):
        super().__init__(blockDict)
Treatment.dispatch["anneal"] = Annealing

class AnnealSection(SingleBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

class AnnealProgram(ListBlock):
    def __init__(self, blockList):
        super().__init__(blockList, AnnealSection)

class TreatmentList(ListBlock):
    def __init__(self, blockList):
        super().__init__(blockList, Treatment)