from .blocks import SingleBlock, ListBlock

from .._debug import Debug

from .._errors import AttachmentTypeError, FileBlockNotFoundError
from .._docs.properties import _validator_rules, val_rules

_debug = Debug()


class Attachment(SingleBlock):
    dispatch_key = "_extension"
    dispatch={} # populated after subclass definitions
    extensions={}
    enforced_subtype=None
    _id_key = "file_name"  
    def __init__(self, blockDict, **kwargs):
        super().__init__(blockDict, **kwargs)
        self._filepath = None

    def __setattr__(self, name, value):
        if name == "_extension":
            if value is None:
                return
            if hasattr(self, "_extension") and value != self._extension:
                from warnings import warn
                warn("You cannot change the extension of an attachment after construction. Skipping change.", RuntimeWarning)
                return

        if name == "file_name":
            old_ext = self._extension if hasattr(self, "_extension") else None
            value, new_ext = self._validate_filename(value, old_ext)
            self._extension = new_ext

        return super().__setattr__(name, value)

    @classmethod
    def _validate_filename(cls, filename:str, ext:str=None, warn=True):
        filename = str(filename)
        if ext is None:
            ext = f".{filename.rsplit('.')[-1]}" if "." in filename else ""
            # delegate to base validator routine to verify extension
            return filename, ext
        
        if "." not in filename:
            new_ext = ext
        else:
            new_ext = f".{filename.rsplit('.')[-1]}"
        
        if new_ext != ext:
            if warn:
                filename = filename + ext
                from warnings import warn
                warn(f"New filename contains a different extension: '{new_ext}'. Extensions cannot "
                    f"be changed after construction. The current extension ('{ext}') "
                    f"will be appended to the new filename to form: '{filename}'.", RuntimeWarning)
            else:
                raise ValueError(f"New filename contains a different extension: '{new_ext}'. Extensions cannot "
                                 "be changed after attachment construction.")
        
        return filename, new_ext

    @classmethod
    def reflex(cls, serialize=True, clean=False, **kwargs:dict):
        from .template import TemplateField
        if "file_name" not in kwargs:
            kwargs["file_name"] = TemplateField.serialize()
            kwargs.pop("path", None)
            add_embedded = "embedded" not in kwargs

        elif not any(k in kwargs for k in ("path", "embedded")):
            add_embedded = True

        if add_embedded:
            kwargs["embedded"] = TemplateField.serialize()

        return super().reflex(serialize=serialize, clean=clean, **kwargs)
    


    def _get_filepath(self):
        """
        Default behavior: Must be overwritten in subclasses.
        """
        raise AttachmentTypeError("Attachments must be constructed as a subclass with a set_filepath method.")


    @classmethod
    def enforce_subtype(cls, subcls, **kwargs):
        # TODO: move enforcement to setattr
        return cls

    @SingleBlock.make_dispatch
    def dispatch_subclass(cls, blockDict, **kwargs):
        from .. import _errors as err
        # just inserted as first line of make_dispatch's dispatcher def
        # blockDict = _unwrap_block(blockDict)

        if "file_name" not in blockDict:
            raise err.MissingPropertyError("file_name", cls, blockDict=blockDict)
        
        _, ext = cls._validate_filename(blockDict["file_name"])

        blockDict[cls.dispatch_key] = ext

        return super(Attachment, cls)
    
        blockDict = blockDict.copy()
        # construct a bare attachment to validate filename and extension
        validated = cls(blockDict, _dispatched=True)

        extension = validated._extension

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

        class NewAttachment(attachmenttype, subtype, cls):
            @classmethod
            def dispatch_subclass(cls, blockDict, **kwargs):
                return cls(blockDict, _dispatched=True, **kwargs)

        return NewAttachment.dispatch_subclass(blockDict, **kwargs)
    
    def find_attachments(self):
        attachments = super().find_attachments()
        if self not in attachments:
            attachments.append(self)

        return attachments
    
class FileType:
    dispatch_key = "_location"
    dispatch = {}
    dispatch_default = None
    dispatch_allow_default = False
    location_classes = {}
    dispatch_from = Attachment

    @Attachment.make_dispatch
    def dispatch_subclass(cls, blockDict, _visited=None, **kwargs):
        from ._blockUtils import _unwrap_block
        from .. import _errors as err

        location = None
        for key, ft in cls.dispatch.items():
            if location is not None:
                blockDict.pop(key, None)
            elif key in blockDict:
                location = key

        if location is None:
            raise err.MissingPropertyError(" or ".join(cls.dispatch.keys()), cls, blockDict=blockDict)

        blockDict[cls.dispatch_key] = location

        # assemble hybrid classes only once
        if location not in cls.location_classes:
            class FileTypeLocator(cls, Attachment):
                dispatch = {}
                dispatch_default = None
                dispatch_allow_default = False

            FileTypeLocator.__name__ = cls.__name__ + "Locator"
            FileTypeLocator.__qualname__ = cls.__name__ + "Locator"
            FileTypeLocator.__module__ = cls.__module__

            cap_loc = location.capitalize()

            for key, ft in cls.dispatch.items():
                class LocatedFileType(ft, cls):
                    dispatch_allow_default = True


                LocatedFileType.__name__ = cap_loc + cls.__name__
                LocatedFileType.__qualname__ = cap_loc + cls.__qualname__
                LocatedFileType.__module__ = cls.__module__

                FileTypeLocator.dispatch[key] = LocatedFileType

            cls.location_classes[location] = FileTypeLocator
        else:
            FileTypeLocator = cls.location_classes[location]

        return super(Attachment, FileTypeLocator)
    
Attachment.dispatch_default = FileType


class CIFFile(FileType, Attachment):
    def __init__(self, blockDict, **kwargs):
        super().__init__(blockDict,**kwargs)
        self._reserved.append("engine")
        self.engine = None
    def _get_engine(self, engine_name=None):
        if engine_name is None:
            if self.engine is None:
                self.engine = self.new_engine()
            engine = self.engine
        else:
            engine = self.new_engine(engine_name=engine_name)

        return engine

    def get_pattern(self, engine_name=None):
        engine = self._get_engine(engine_name=engine_name)

        return engine.get_pattern()
    
    def get_peaks(self, engine_name=None):
        engine = self._get_engine(engine_name=engine_name)

        return engine.get_peaks()
    
    def new_engine(self, engine_name=None):
        from ..config import values as cfg
        from ..plotting.diffraction.engines import ENGINES
        if engine_name is None:
            engine_name = cfg.get("diffraction.default_engine")
        return ENGINES[engine_name](self._get_filepath())

    def quick_pattern(self,subprocess=False):
        from ..plotting._utils import _quick_pattern
        
        df = self.get_pattern()

        x,y = df.columns[:2]

        tth, intensity = df[x].to_numpy(), df[y].to_numpy()

        if subprocess:
            return self._subprocess(_quick_pattern, args=(tth, intensity))
        
        return _quick_pattern(tth, intensity)
    
Attachment.dispatch[".cif"] = CIFFile

class LocationType:
    dispatch = {}
    @Attachment.make_dispatch
    def dispatch_subclass(cls, blockDict, _visited=None, **kwargs):
        return super(Attachment, cls)


class EmbeddedFile(LocationType, Attachment):
    def _write_to_temp(self, encoding="utf-8"):
        try:
            temppath = self.find_temppath()
        except Exception as e:
            _debug.msg(f"Could not find a temporary path to write to.\n{e}")
            return None
        filepath = temppath / self.file_name()
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
        #serial["embedded"] = self.embedded.copy()
        return serial
FileType.dispatch["embedded"] = EmbeddedFile

class PathFile(LocationType, Attachment):
    def __init__(self, blockDict, **kwargs):
        super().__init__(blockDict, **kwargs)
        

    def _get_abspath(self):
        filedir = self._get_filedir().resolve()

        return (filedir / str(self.path) / self.file_name()).resolve()
    
    def _get_filedir(self):
        from pathlib import Path
        fileblock = self.find_fileblock()
        return Path(fileblock._sourceFile).parent.resolve()

    def exists(self):
        return self._filepath.is_file() if self._filepath is not None else False
    
    def refresh(self, new_copy="prompt",overwrite="prompt", **kwargs):
        from .. import cfg
        try:
            if self._filepath is None:
                self._get_filepath(rf_new_copy=new_copy, rf_overwrite=overwrite, **kwargs)
                return
            if not self.exists():
                raise ValueError(f"Cannot find file at last known location of attachment: {self._filepath}")

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
                    new_path = self._filepath.parent.resolve().relative_to(self._get_filedir(),walk_up=True)
                    self.path = str(new_path)

            checkpath = self._get_abspath()
            check = checkpath.is_file()
            if not check:  
                raise ValueError(f"Could not successfully refresh attachment to location: {checkpath}.")
            
            self._filepath = checkpath

        except Exception as e:
            if not cfg.track_attachments.ignore:
                raise e
            else:
                _debug.msg(f"Could not refresh attachment: {e}. Configured to ignore.")

    def change_path(self, new_path):
        from pathlib import Path
        import warnings
        abspath = Path(new_path).resolve()

        parent = abspath.parent
        filename = abspath.name
        ext = self._extension if hasattr(self, "_extension") else None

        warnings.simplefilter("always")
        filename, ext = self._validate_filename(filename, ext, warn=False) 
        abspath = parent / filename

        if not abspath.is_file():
            raise ValueError(f"Cannot change path to file that does not exist: {abspath}")
        
        self.file_name = filename
        self.path = str(abspath.parent.relative_to(self._get_filedir(),walk_up=True))
        self._filepath = abspath
        self.refresh()
    
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
        
        
FileType.dispatch["path"] = PathFile


CifList = ListBlock.Simple(CIFFile)