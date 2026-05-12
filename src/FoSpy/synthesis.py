from FoSpy.parsing import parse_FOS

class Synthesis:
    def __init__(self, blockDict):
        self.sourceFile = blockDict.get("sourceFile")

    
    @classmethod
    def fromFile(cls, filepath):
        blockDict = parse_FOS(filepath)
        return cls(blockDict)