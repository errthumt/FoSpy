from FoSpy.blocks.blocks import ListBlock

from .blocks import SingleBlock

from .._debug import Debug
_debug = Debug()

class EmbeddedFile(SingleBlock):
    """
    Represents an non-FOS file embedded as a block in a FOS file.
    """
    def _write_to_temp(self, encoding="utf-8"):
        self._temppath = self.find_temppath() / f"{self.file_name}{self.extension}"
        with open(self._temppath, "w", encoding=encoding) as f:
            for line in self.embedded:
                f.write(line.rstrip("\r\n") + "\n")

     
    def serialize(self,keepListType=False, clean=False):
        """
        Performs the default `SingleBlock` serialization, but restores the
        "embedded" key to the full list of embedded lines instead of a string.
        """
        serial = super().serialize(keepListType, clean=clean)
        serial["embedded"] = self.embedded.copy()
        return serial

class EmbeddedCIF(EmbeddedFile):
    """
    Represents a CIF file embedded as a block in a FOS file.
    """

    def get_pattern(self,**kwargs):
        from cif2xrd.pattern import simPattern
        self._write_to_temp()

        sim = simPattern(cif_path=self._temppath, **kwargs)

        return sim.two_theta, sim.intensity
    
    def quick_pattern(self,subprocess=False, **kwargs):
        import matplotlib.pyplot as plt
        from ..plotting.EmbeddedCIF import _quick_pattern
        two_theta, intensity = self.get_pattern(**kwargs)

        if subprocess:
            return self._subprocess(_quick_pattern,args=(two_theta, intensity))
        
        return _quick_pattern(two_theta, intensity)


CifList = ListBlock.Simple(EmbeddedCIF)
"""
A [simple list][FoSpy.blocks.blocks.ListBlock.Simple] of
[`EmbeddedCIF` objects][FoSpy.blocks.embedded.EmbeddedCIF].
"""

from ._blockUtils import _get_block_classes
import sys
__block_classes__ = _get_block_classes(sys.modules[__name__])
"""List of all [`Block`][FoSpy.blocks.blocks.Block] classes defined in this module.
Used for generating documentation site."""
