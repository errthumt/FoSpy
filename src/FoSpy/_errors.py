# TODO: Figure out cleaner type hints without circular imports.

class AttachmentTypeError(Exception):
    pass


class FileBlockNotFoundError(Exception):
    pass

def _summarize_exception_group(exc: Exception, indent: int = 0) -> list[str]:
    """Return a list of summary lines for an ExceptionGroup or PropertyError."""
    pad = "  " * indent
    lines = []

    if hasattr(exc, "summary"):
        lines.append(f"{pad}{exc.summary}")
        indent += 1
    
    if hasattr(exc, "cause"):
        lines.extend(_summarize_exception_group(exc.cause, indent))
    
    elif isinstance(exc, ExceptionGroup):
        for e in exc.exceptions:
            lines.extend(_summarize_exception_group(e, indent))

    elif not hasattr(exc, "summary"):
        msg = exc.args[0].strip().split("\n",1)[0]
        msg = msg[:60] + "..." if len(msg) > 80 else msg
        lines.append(f"{pad}{msg}")
    
    return lines

class MultipleErrors(ExceptionGroup):
    pass

class PropertyError(Exception):
    def __init__(self, key, blockObj, *args, blockDict={}, hint="Error for property: ", **kwargs):
        typ_nm, block_id, id_key = _get_block_info(blockObj, blockDict)

        hint += f"'{key}' for '{typ_nm}' object."
        if block_id is not None:
            hint += f" (ID: {id_key} = {block_id})"

        super().__init__(hint, *args, **kwargs)

        self.summary = f"Error on '{key}'"


def _get_block_info(blockObj, blockDict={}):
    typ = type(blockObj)
    typ_nm = typ.__name__

    if hasattr(typ, "_id_key"):
        id_key = typ._id_key
        block_id = blockDict.get(id_key, None)
    else:
        id_key = None
        block_id = None

    return typ_nm, block_id, id_key

class MultiplePropertyErrors(MultipleErrors, PropertyError):
    pass

def PropertyErrorGroup(blockObj, blockDict={}, errors=[]):
    typ_nm, block_id, id_key = _get_block_info(blockObj, blockDict)

    hint = f"Property Error(s) occurred when trying to construct '{typ_nm}' object."

    if block_id is not None:
        hint += f" (ID: {id_key} = {block_id})"

    hint += "\n\n===Summary===\n"
    for error in errors:
        hint += "\n".join(_summarize_exception_group(error)) + "\n"

    return MultiplePropertyErrors(hint, errors)



class MissingPropertyError(PropertyError):
    def __init__(self, key, blockObj, *args, blockDict={}, hint="Missing required property: ", **kwargs):
        super().__init__(key, blockObj, *args, blockDict=blockDict, hint=hint, **kwargs)
        self.summary = f"Missing '{key}'"

class FailedValidatorError(PropertyError):
    def __init__(self, key, blockObj, cause:Exception, *args, blockDict={}, **kwargs):
        
        super().__init__(key, blockObj, *args, blockDict=blockDict, hint="Failed to validate property: ", **kwargs)

        self.cause = cause

        self.__cause__ = cause
        self.summary = f"Failed to validate '{key}'"

class PropertyAliasError(PropertyError):
    def __init__(self, key, blockObj, *args, blockDict={}, hint="Problem with aliased property: ", posthint:str=None, **kwargs):
        super().__init__(key, blockObj, *args, blockDict=blockDict, hint=hint, **kwargs)
        if posthint is not None:
            self.args[0] += "\n" + posthint

        self.summary = f"Alias error for '{key}'"

class ListBlockError(Exception):
    def __init__(self, blockObj, *args, hint="Error constructing ListBlock", posthint:str=None, **kwargs):
        self.blockObj = blockObj
        self.typ_nm, _, _ = _get_block_info(blockObj)
        self.hint = hint
        self.posthint = posthint
        self._build_hint()

        super().__init__(self.hint, *args, **kwargs)
        self.summary = f"Error constructing '{self.typ_nm}'."

    def _build_hint(self):
        self._build_prehint()
        self._build_posthint()

    def _build_prehint(self):
        self.hint += f" ({self.typ_nm} Type)"
    
    def _build_posthint(self):
        self.hint += f":\n{self.posthint}"


class ListBlockMismatchError(ListBlockError):
    def __init__(self, blockObj, candidate, idx:int, *args, hint="Error adding block to ListBlock:", posthint:str=None, cause:Exception=None, **kwargs):
        self.candidate = candidate


        super().__init__(blockObj, *args, hint=hint, **kwargs)

        self.summary = f"(Index: {idx})"

        if cause is not None:
            self.__cause__ = cause
            self.cause = cause

    def _build_prehint(self):
        self.hint += f"\nCandidate:\n{self.candidate}\nis not a valid entry for this list block"
        super()._build_prehint()

    def _build_posthint(self):
        typ_nm = self.blockObj._reqCls.__name__
        self.hint += f"\nCandidates must be coersible to {typ_nm} objects."
        super()._build_posthint()

class MultipleListBlockErrors(MultipleErrors, ListBlockError):
    pass

def ListBlockErrorGroup(blockObj, errors=[]):
    typ_nm, _, _ = _get_block_info(blockObj)
    return MultipleListBlockErrors(f"Error(s) occurred when trying to construct or modify '{typ_nm}' object.", errors)
