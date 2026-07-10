import re
from ..._debug import Debug
from pathlib import Path
from ..._docs.properties import _validator_rules
_debug = Debug()
_debug.on = True

# Allowed filename characters (no slashes)
FILENAME_RE = re.compile(r"^[A-Za-z0-9._\-,]+$")

basePath = type(Path(""))

@_validator_rules(
    "Mutually exclusive with `embedded` property.",
    "A valid relative filepath to a directory.",
    "Path is relative to the directory containing the parent `FileBlock`.",
    '"`.`" should be used to indicate the same directory as the parent `FileBlock`.',
    '"`..`" can be used to walk up the directory tree.',
    "Paths to nonexistent directories will be validated, but may raise errors when the parent `FileBlock` attempts to track the file.",
    "Examples for a `FileBlock` at `/home/user/synthesis.fos`:", [
        "\"`.`\" is `/home/user`",
        "\"`..`\" is `/home`",
        "\"`../foo`\" is `/home/foo`",
        "\"`./bar`\" is `/home/user/bar`",
    ]
)
class PathPosix(basePath):
    def __init__(self, path):
        path = path.replace("%20", " ")
        super().__init__(path)
    def serialize(self, *args, **kwargs):
        return self.as_posix().replace(" ", "%20")
    

@_validator_rules(
    "Mutually exclusive with `path` property.",
    "Attachment content as a raw `utf-8` string."
)
def embedded(txt):
    return str(txt)


@_validator_rules(
    "A valid filename (no path, no separators, allowed characters only).",
    "Must include a valid extension.",
    "Allowed characters: letters, digits, '`_`', '`-`', '`.`'",
    "Commas are allowed, but may lead to unexpected behavior for some OS or software.",
    "Paths to nonexistent files will be validated, but may raise errors when the parent `FileBlock` attempts to track the file."
)
def file_name(name: str, sourceDict={}) -> str:
    """
    Validate a filename (no path, no separators, allowed characters only).
    """
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
    
    if len(name.split(".")) < 2 or name.split(".")[1] == "":
        raise ValueError("Filename must have an extension")

    return name

EXT_RE = re.compile(r"^[A-Za-z0-9_-]+$")  # no dots allowed inside

# def file_extension(ext: str) -> str:
#     """
#     Validate a file extension.
#     Accepts either 'png' or '.png' and normalizes to '.png'.
#     """
#     if not isinstance(ext, str):
#         raise TypeError("Extension must be a string")

#     if not ext:
#         raise ValueError("Extension cannot be empty")

#     # Normalize: strip leading dot if present
#     if ext.startswith("."):
#         ext = ext[1:]

#     # Validate characters
#     if not EXT_RE.match(ext):
#         raise ValueError(
#             "Extension contains invalid characters. Allowed: letters, digits, '_', '-'"
#         )

#     return f".{ext}"


    
