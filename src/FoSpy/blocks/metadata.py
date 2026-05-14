from . import SingleBlock, ListBlock

class MetaData(SingleBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

class Reaction(SingleBlock):
    def __init__(self, blockDict):
        #placeholder assignment
        self.nominal_mass = blockDict["nominal_mass"]
        super().__init__(blockDict)


class Experimenter(SingleBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

class ExperimenterList(ListBlock):
    def __init__(self, blockList):
        super().__init__(blockList, Experimenter)