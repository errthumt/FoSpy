from .blocks import SingleBlock, ListBlock

from .._debug import Debug
_debug = Debug()

class AttachmentTypeError(Exception):
    pass

class Attachment(SingleBlock):
    dispatch={}
    extensions={}
    enforced_subtype=None  
    def __init__(self, blockDict, **kwargs):
        super().__init__(blockDict, **kwargs)
        self._filepath = None

    def _get_filepath(self):
        """
        Default behavior: Must be overwritten in subclasses.
        """
        raise AttachmentTypeError("Attachments must be constructed as a subclass with a set_filepath method.")


    @classmethod
    def enforce_subtype(cls, subcls, **kwargs):
        class EnforcedAttachment(cls):
            enforced_subtype = subcls
            pass
        return EnforcedAttachment

    @classmethod
    def dispatch_subclass(cls, blockDict, **kwargs):
        blockDict = blockDict.copy()
        # construct a bare attachment to validate filename and extension
        validated = cls(blockDict, _dispatched=True)

        extension = validated.extension()

        attachmenttype = None
        for key, ft in cls.dispatch.items():
            if attachmenttype is not None:
                blockDict.pop(key, None)
            elif key in blockDict:
                attachmenttype = ft

        if attachmenttype is None:
            raise ValueError(f"Could not determine type for attachment: {validated.file_name}. "
                             f"Must have one of the following keys: {list(cls.dispatch.keys())}") 
        
        subtype = cls.extensions.get(extension, cls)

        if cls.enforced_subtype is not None and not issubclass(subtype, cls.enforced_subtype):
            raise ValueError(f"Attachment type for this key must be a subclass of {cls.enforced_subtype.__name__}")

        class NewAttachment(attachmenttype, subtype):
            @classmethod
            def dispatch_subclass(cls, blockDict, **kwargs):
                return cls(blockDict, _dispatched=True, **kwargs)

        return NewAttachment.dispatch_subclass(blockDict, **kwargs)

class EmbeddedFile(Attachment):
    def _write_to_temp(self, encoding="utf-8"):
        try:
            temppath = self.find_temppath()
        except Exception as e:
            _debug.msg(f"Could not find a temporary path to write to.\n{e}")
            return None
        filepath = temppath / f"{self.file_name}{self.extension}"
        with open(filepath, "w", encoding=encoding) as f:
            for line in self.embedded:
                f.write(line.rstrip("\r\n") + "\n")
        _debug.msg(f"Successfully wrote embedded file to temporary path: {filepath}")
        return filepath

    def _get_filepath(self):
        if self._filepath is not None:
            return self._filepath
        return self._write_to_temp()
     
    def serialize(self,**kwargs):
        """
        Performs the default `SingleBlock` serialization, but restores the
        "embedded" key to the full list of embedded lines instead of a string.
        """
        serial = super().serialize(**kwargs)
        serial["embedded"] = self.embedded.copy()
        return serial
Attachment.dispatch["embedded"] = EmbeddedFile

class CIFFile(Attachment):
    def get_pattern(self,**kwargs):
        from cif2xrd.pattern import simPattern

        sim = simPattern(cif_path=self._get_filepath(), **kwargs)

        return sim.two_theta, sim.intensity
    
    def quick_pattern(self,subprocess=False, **kwargs):
        import matplotlib.pyplot as plt
        from ..plotting.EmbeddedCIF import _quick_pattern
        two_theta, intensity = self.get_pattern(**kwargs)

        if subprocess:
            return self._subprocess(_quick_pattern,args=(two_theta, intensity))
        
        return _quick_pattern(two_theta, intensity)

Attachment.extensions[".cif"] = CIFFile

CifList = ListBlock.Simple(Attachment.enforce_subtype(CIFFile))