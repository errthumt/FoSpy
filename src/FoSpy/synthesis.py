from .parsing import (
    dict_from_file,
    write_dict_to_file
)
from .parsing import syntax as st


class Synthesis:
    def __init__(self, blocksDict, _sourceFile=None):
        self.blocks = blocksDict.copy()
        self.meta = self.blocks.pop("metadata") # needs validation routine
        self._comments = self.blocks.pop(st.comment_key)

        self.materials = self.blocks.pop("Materials") # needs validation routine
        self.treatments = self.blocks.pop("Treatments") # needs validation routine

    @classmethod
    def fromFile(cls, filepath):
        blocksDict = dict_from_file(filepath)
        return cls(blocksDict, _sourceFile = filepath)
    

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

        write_dict_to_file(blocksDict, filepath)


        