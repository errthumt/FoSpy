from FoSpy.parsing import read_FOS, write_FOS

class Synthesis:
    def __init__(self, blocksDict):
        self.blocks = blocksDict.copy()
        self.meta = self.blocks.pop("meta") # needs validation routine
        self._sourceFile = self.blocks.pop("sourceFile")
        self._comments = self.blocks.pop("comments")

        self.materials = self.blocks.pop("materials") # needs validation routine
        self.treatments = self.blocks.pop("treatments") # needs validation routine

    @classmethod
    def fromFile(cls, filepath):
        blocksDict = read_FOS(filepath)
        return cls(blocksDict)
    

    def insert_material(self, mat, idx=-1):
        # placeholder. modify for insertion at idx
        self.materials.append(mat)

    def insert_treatment(self, treat, idx=-1):
        # placeholder. modify for insertion at idx
        self.treatments.append(treat)

    def serialize(self):
        """
            Placeholder.
            Recurse through blocks and serialize when necessary
            Return dictionary
        """
        return {}
    
    def save(self, filepath=None):
        if filepath is None:
            if self._sourceFile is None:
                raise ValueError("Synthesis object was constructed without a sourceFile. A save destination must be specified.")
            else:
                filepath = self._sourceFile
        
        self._sourceFile = filepath
        blocksDict = self.serialize()

        write_FOS(blocksDict, filepath)


        