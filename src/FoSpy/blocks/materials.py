from . import SingleBlock, ListBlock

class Material(SingleBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

class MaterialList(ListBlock):
    def __init__(self, blockList):
        super().__init__(blockList, Material)