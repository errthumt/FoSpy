from .parsing import (
    dict_from_file,
    write_dict_to_file
)
from .parsing import syntax as snt
from .blocks import SingleBlock

class Synthesis(SingleBlock):
    def __init__(self, blockDict, _sourceFile=None):
        blockDict = blockDict.copy()
        self._comments = blockDict.pop(snt.meta_keys["comments"])
        super().__init__(blockDict)

    @classmethod
    def fromFile(cls, filepath):
        blockDict = dict_from_file(filepath)
        return cls(blockDict, _sourceFile = filepath)
    

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
        blockDict = self.serialize()

        write_dict_to_file(blockDict, filepath)


        