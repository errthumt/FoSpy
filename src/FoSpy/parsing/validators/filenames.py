import re
from ..._debug import Debug
from pathlib import Path
_debug = Debug()
_debug.on = True

# Allowed filename characters (no slashes)
FILENAME_RE = re.compile(r"^[A-Za-z0-9._\-,]+$")

basePath = type(Path(""))

class PathPosix(basePath):
    def serialize(self, *args, **kwargs):
        return self.as_posix()

    


def file_name(name: str, sourceDict={}) -> str:
    """
    Validate a filename (no path, no separators, allowed characters only).
    """
    #_debug.pmsg(f"Validating {name} with dict:")
    #_debug.pmsg(sourceDict)
    if "extension" in sourceDict:
        ext = file_extension(sourceDict["extension"])
        if name.endswith(ext):
            new_name = name[:-len(ext)]
            _debug.msg(f"Converted filename: {name} into {new_name}")
            name = new_name

    if not isinstance(name, str):
        raise TypeError("Filename must be a string")

    if not name:
        raise ValueError("Filename cannot be empty")

    if "/" in name or "\\" in name:
        raise ValueError("Filename must not contain path separators")

    if "," in name:
        from warnings import warn
        warn(f"Comma in embedded filename: '{name}' may lead to unexpected behavior.",SyntaxWarning)

    if not FILENAME_RE.match(name):
        raise ValueError(
            "Filename contains invalid characters. Allowed: letters, digits, '_', '-', '.'"
        )

    return name

EXT_RE = re.compile(r"^[A-Za-z0-9_-]+$")  # no dots allowed inside

def file_extension(ext: str) -> str:
    """
    Validate a file extension.
    Accepts either 'png' or '.png' and normalizes to '.png'.
    """
    if not isinstance(ext, str):
        raise TypeError("Extension must be a string")

    if not ext:
        raise ValueError("Extension cannot be empty")

    # Normalize: strip leading dot if present
    if ext.startswith("."):
        ext = ext[1:]

    # Validate characters
    if not EXT_RE.match(ext):
        raise ValueError(
            "Extension contains invalid characters. Allowed: letters, digits, '_', '-'"
        )

    return f".{ext}"


    
