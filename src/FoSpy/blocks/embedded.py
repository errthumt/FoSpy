from .blocks import SingleBlock, ListBlock

class EmbeddedFile(SingleBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

class EmbeddedCIF(EmbeddedFile):
    def __init__(self, blockDict):
        super().__init__(blockDict)

class CIFList(ListBlock):
    def __init__(self, blockList):
        super().__init__(blockList, EmbeddedCIF)