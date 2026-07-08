from .blocks import SingleBlock
from ..parsing.read import dict_from_file
from ..parsing.write import write_dict_to_file
from .. import _errors as err


import atexit
import json
import os
import tempfile
import shutil
from pathlib import Path

temp_dirs = []

def _clear_path_contents(path:Path):
    if not path.exists():
        return
    
    if not path.is_dir():
        raise NotADirectoryError(path)
    
    for item in path.iterdir():
        try:
            if item.is_dir() and not item.is_symlink():
                shutil.rmtree(item)
        except Exception as e:
            raise Exception("Failed to remove directory") from e

def save_fosx(blockDict, filepath, **kwargs):
    tempdir = tempfile.TemporaryDirectory()
    atexit.register(tempdir.cleanup)

    tempdir = Path(tempdir.name)
    tempdir.mkdir(exist_ok=True)

    temp_path = tempdir / "~temp~.fos"
    write_dict_to_file(blockDict, temp_path, **kwargs)

    new_file = FileBlock.fromFile(temp_path)
    new_file.package(filepath)

def _get_ext_dir(fosx_path):
    val_path = Path(fosx_path)
    parent = val_path.parent

    i = 0
    ext_dir = None
    while (ext_dir is None or 
        (str(ext_dir) in temp_dirs and ext_dir.exists())):
        i += 1
        stem = f"~.{i}{val_path.stem}"
        ext_dir = parent / stem

    ext_dir.mkdir(exist_ok=True)
    _clear_path_contents(ext_dir)
    temp_dirs.append(str(ext_dir))
    atexit.register(lambda d=ext_dir: shutil.rmtree(d))

    fos_path = ext_dir / (val_path.stem + ".fos")

    return ext_dir, fos_path

def open_fosx(fosx_path, **kwargs):
    ext_dir, fos_path = _get_ext_dir(fosx_path)

    shutil.unpack_archive(
        filename=fosx_path,
        extract_dir=ext_dir,
        format="zip"
    )
    
    load = FileBlock.fromFile(fos_path)
    return load.serialize()

EXT_MAP = {
    "fos": (dict_from_file, write_dict_to_file),
    "fosx": (open_fosx, save_fosx),
    "json": (
        lambda fp: json.load(open(fp, "r")),
        lambda blockDict, fp, **kwargs: 
            json.dump(blockDict, open(fp, "w"), indent=kwargs.pop("json_indent",4), **kwargs)
    )
}

EXT_READ_MAP = {
    k: v[0] for k, v in EXT_MAP.items()
}

EXT_WRITE_MAP = {
    k: v[1] for k, v in EXT_MAP.items()
}

class FileBlock(SingleBlock):
    """
    Represents a set of blocks loaded from a file.

    All public attributes of `FileBlock` objects are either `SingleBlock` or
    `ListBlock` objects. Attributes without a header at the start of the file
    are parsed into `{"metadata": blockDict}` before passing to `FileBlock`.

    Noteable Subclasses:
    ```
    Synthesis(FileBlock)
    TemplateSet(FileBlock)
    ```
    """

    def __init__(self, blockDict, _sourceFile=None, _dispatched=True):
        """
        Optionally specify _sourceFile before constructing from blockDict using parent `SingleBlock` constructor.
        """
        self._sourceFile = _sourceFile

        self._tempdir = tempfile.TemporaryDirectory()
        self._temppath = Path(self._tempdir.name)
        atexit.register(self.cleanup)

        super().__init__(blockDict, _dispatched=_dispatched)
        self.refresh_attachments()

    def __setattr__(self, name, value):
        if name == "_sourceFile":
            if str(value).endswith(".fosx"):
                self._ext_file = value
                self._ext_dir, value = _get_ext_dir(value)
            else:
                self._ext_file = None
                self._ext_dir = None
        super().__setattr__(name, value)         

    def cleanup(self):
        if self._tempdir is not None:
            self._tempdir.cleanup()

    def get_id(self):
        try:
            if self._sourceFile is not None:
                from pathlib import Path
                fp = Path(self._sourceFile)
                return "file_name", str(fp.name)
            else:
                return "file_name", "<Unsaved FileBlock>"
        except Exception:
            return super().get_id()

    @classmethod
    def fromFile(cls, filepath):
        from .metadata import MetaData
        from ._blockUtils import _unwrap_block
        abspath = os.path.abspath(filepath)
        pathstr = str(abspath)
        try:
            ext = pathstr.lower().split(".")[-1]
        except IndexError:
            raise ValueError(f"Could not determine extension for filepath: {pathstr}")

        if ext not in EXT_READ_MAP:
            raise ValueError(f"Unrecognized file extension '{ext}'. Supported extensions are: {list(EXT_READ_MAP.keys())}")

        blockDict = EXT_READ_MAP[ext](abspath)
        if "metadata" not in blockDict:
            raise err.MissingPropertyError("metadata", cls, blockDict=blockDict)
        
        metadata = _unwrap_block(blockDict["metadata"])
        if "fos_type" not in metadata:
            # Metadata construction will always fail, delegate error message to construction
            try:
                from .metadata import MetaData
                _ = MetaData(metadata)
            except Exception as e:
                raise ValueError(f"Could not open file due to the following errors when validating metadata block:\n{e}")


        typ = metadata.get("fos_type","").lower()
        subcls = MetaData.dispatch.get(typ, ("", cls))[1]

        if not issubclass(subcls, cls):
            raise ValueError(f"Cannot construct {cls.__name__} from file '{abspath}' with incompatible fos_type '{typ}'.")

        return subcls.dispatch_subclass(blockDict, _sourceFile = abspath)

    def save(self, filepath:str=None, json_indent=4, **kwargs):
        """
        Sends a serialized dict to be written to file.

        Args:
            filepath:
                If specified, writes serialized dict to filepath. ks to `self._sourceFile`.
            json_indent:
                Indent to use for json.dump when saving as json
            **kwargs:
                Optional kwargs to pass to saving routine (unique to each file extension)

        Raises:
            ValueError:
                If _sourceFile is not specified (if `FileBlock` was copied from
                another object or constructed directly from a blockDict),
                filepath must be specified.
        """
        from warnings import warn
        saving_as = filepath is not None
        try:
            if not saving_as:
                if self._sourceFile is None:
                    raise ValueError("Synthesis object was constructed without a sourceFile. A save destination must be specified.")
                else:
                    filepath = self._sourceFile
            self._sourceFile = os.path.abspath(filepath)

            filepath = self._sourceFile if self._ext_file is None else self._ext_file
            if str(filepath).endswith(".fosx"):
                return self.package(filepath)
            self.refresh_attachments()
            pathstr = str(filepath)
            try:
                ext = pathstr.lower().split(".")[-1]
            except IndexError:
                raise ValueError(f"Could not determine extension for filepath: {pathstr}")


            ext = str(filepath).lower().split(".")[-1]

            if ext not in EXT_WRITE_MAP:
                raise ValueError(f"Unrecognized file extension '{ext}'. Supported extensions are: {list(EXT_WRITE_MAP.keys())}")

            blockDict = self.serialize(clean="fos" not in ext)

            EXT_WRITE_MAP[ext](blockDict, filepath, json_indent=json_indent, **kwargs)

        except Exception as e:
            if not saving_as:
                warn(f"Could not save file. Disconnected from source file for safety. Exception: {e}", RuntimeWarning)
                self._sourceFile = None
                return e
            else:
                raise e
        return True
    
    def copy(self):
        """
        Returns a deep copy of self by saving to a temp file and reloading.

        Save/Reload allows attachment tracking to remain intact where
        serialization/reconstruction would normally desync.
        """
        # get temporary save location
        loc = self._temppath / "~temp~.fos"

        # cache current source file
        src = self._sourceFile

        # save and restore cached source file
        self.save(loc)
        self._sourceFile = src

        # load copy from temp file
        copy = self.fromFile(loc)
        # desync copy from temp file
        copy._sourceFile = None
        return copy
    
    def check_attachments(self):
        pass

    def matches_file(self):
        reloaded = self.fromFile(self._sourceFile)

        return self.__eq__(reloaded, suppress_routine_paths=True)
    
    def package(self, pkg_fp):
        import shutil
        pkg_fp = Path(pkg_fp)
        pkg_dir = self._temppath / "~package~"
        pkg_dir.mkdir(exist_ok=True)

        attachment_dir = pkg_dir / "attachments"
        attachment_dir.mkdir(exist_ok=True)

        copy = self.copy()

        for attachment in copy.find_attachments():
            attachment.path = "attachments"

        copy._sourceFile = pkg_dir / (pkg_fp.stem + ".fos")
        copy.refresh_attachments(new_copy=True, overwrite=False)
        copy.save()

        pkg_fp = pkg_fp.parent / pkg_fp.stem
        fosx_fp = pkg_fp.with_suffix(".fosx")
        zip_fp = Path(shutil.make_archive(pkg_fp, "zip", pkg_dir))

        if fosx_fp.exists():
            fosx_fp.unlink()

        zip_fp.rename(fosx_fp)

        shutil.rmtree(pkg_dir)


    