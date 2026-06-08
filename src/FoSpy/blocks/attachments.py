from .blocks import SingleBlock, ListBlock

from .._debug import Debug
_debug = Debug()

from .._errors import AttachmentTypeError, FileBlockNotFoundError



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

class PathFile(Attachment):
    def __init__(self, blockDict, **kwargs):
        super().__init__(blockDict, **kwargs)
        

    def _get_abspath(self):
        filedir = self._get_filedir()

        return filedir / str(self.path) / f"{self.file_name}{self.extension}"
    
    def _get_filedir(self):
        from pathlib import Path
        fileblock = self.find_fileblock()
        return Path(fileblock._sourceFile).parent

    def exists(self):
        return self._filepath.is_file() if self._filepath is not None else False
    
    def refresh(self, new_copy="prompt",overwrite="prompt", **kwargs):
        if self._filepath is None:
            self._get_filepath(rf_new_copy=new_copy, rf_overwrite=overwrite, **kwargs)
            return
        if not self.exists():
            raise ValueError(f"Cannot find file at last known location of attachment: {self._filepath}")
        
        if new_copy != "prompt" and not isinstance(new_copy, bool):
            raise ValueError("new_copy must be a boolean or 'prompt'")
        
        if overwrite != "prompt" and not isinstance(overwrite, bool):
            raise ValueError("overwrite must be a boolean or 'prompt'")

        new_path = self._get_abspath()
        if self._filepath != new_path:
            printmsg = f"Attachment file path has changed: {self._filepath} -> {new_path}"
            prompted=False
            if new_copy == "prompt":
                print(printmsg)
                prompted=True
            
            if new_copy == "prompt":
                new_copy = input("You can copy the file to the new location, "
                                 "or modify the path value to match the old location. "
                                 "Copy? (y/n): ").lower() == "y"
                
            if new_copy:
                if new_path.is_file() and overwrite == "prompt":
                    if not prompted:
                        print(printmsg)
                    overwrite = input("File already exists at new location. "
                                      "Overwrite? (y/n): ").lower() == "y"
                if overwrite or not new_path.is_file():
                    import shutil
                    shutil.copyfile(self._filepath, new_path)
                    self._filepath = new_path

            else:
                new_path = self._filepath.parent.relative_to(self._get_filedir(),walk_up=True)
                self.path = str(new_path)

        checkpath = self._get_abspath()
        check = checkpath.is_file()
        if not check:  
            raise ValueError(f"Could not successfully refresh attachment to location: {checkpath}.")
        
        self._filepath = checkpath

    
    def _get_filepath(self, rf_new_copy=False, rf_overwrite=False, **kwargs):
        if self._filepath is None:
            try:
                self._filepath = self._get_abspath()
            except FileBlockNotFoundError:
                self._filepath = None
        else:
            self.refresh(new_copy=rf_new_copy, overwrite=rf_overwrite, **kwargs)
        return self._filepath
    
    def copy(self):
        copy = super().copy()
        copy._filepath = self._filepath
        return copy
        
        
Attachment.dispatch["path"] = PathFile

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