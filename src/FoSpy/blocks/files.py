from .blocks import SingleBlock
from ..parsing.read import dict_from_file
from ..parsing.write import write_dict_to_file
from .. import _errors as err


import atexit
import json
import os
import tempfile
from pathlib import Path


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

    def cleanup(self):
        if self._tempdir is not None:
            self._tempdir.cleanup()

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

        ext_map = {
            "fos": dict_from_file,
            "json": lambda fp: json.load(open(fp, "r"))
        }

        if ext not in ext_map:
            raise ValueError(f"Unrecognized file extension '{ext}'. Supported extensions are: {list(ext_map.keys())}")

        blockDict = ext_map[ext](abspath)
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
            self.refresh_attachments()
            pathstr = str(self._sourceFile)
            try:
                ext = pathstr.lower().split(".")[-1]
            except IndexError:
                raise ValueError(f"Could not determine extension for filepath: {pathstr}")

            ext_map = {
                "fos": write_dict_to_file,
                "json": lambda blockDict, fp, **kwargs: json.dump(blockDict, open(fp, "w"), indent=json_indent, **kwargs)
            }

            ext = str(filepath).lower().split(".")[-1]

            if ext not in ext_map:
                raise ValueError(f"Unrecognized file extension '{ext}'. Supported extensions are: {list(ext_map.keys())}")

            blockDict = self.serialize(clean=ext!="fos")

            ext_map[ext](blockDict, self._sourceFile, **kwargs)

        except Exception as e:
            if not saving_as:
                warn(f"Could not save file. Disconnected from source file for safety. Exception: {e}", RuntimeWarning)
                self._sourceFile = None
                return e
            else:
                raise e
        return True
    
    def check_attachments(self):
        pass

    def matches_file(self):
        reloaded = self.fromFile(self._sourceFile)

        return self.__eq__(reloaded, suppress_routine_paths=True)
    