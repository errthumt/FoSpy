from .blocks.blocks import SingleBlock, ListBlock, Block

class AttachmentTypeError(Exception):
    pass


class FileBlockNotFoundError(Exception):
    pass

class PropertyError(Exception):
    def __init__(self, key, blockObj:SingleBlock, *args, blockDict={}, hint="Error for property: ", **kwargs):
        typ_nm, block_id, id_key = _get_block_info(blockObj, blockDict)

        hint += f"'{key}' for '{typ_nm}' object."
        if block_id is not None:
            hint += f" (ID: {id_key} = {block_id})"

        super().__init__(hint, *args, **kwargs)


def _get_block_info(blockObj:Block, blockDict={}):
    typ = type(blockObj)
    typ_nm = typ.__name__

    if hasattr(typ, "id_key"):
        id_key = typ.id_key
        block_id = blockDict.get(id_key, None)
    else:
        block_id = None

    return typ_nm, block_id, id_key

class PropertyErrorGroup(ExceptionGroup, PropertyError):
    def __init__(self, blockObj:SingleBlock, blockDict={}, errors=[]):
        typ_nm, block_id, id_key = _get_block_info(blockObj, blockDict)

        hint = f"Property Error(s) occurred when trying to construct '{typ_nm}' object."

        if block_id is not None:
            hint += f" (ID: {id_key} = {block_id})"

        super().__init__(hint, errors)



class MissingPropertyError(PropertyError):
    def __init__(self, key, blockObj:SingleBlock, *args, blockDict={}, **kwargs):
        super().__init__(key, blockObj, *args, blockDict=blockDict, hint="Missing required property: ", **kwargs)

class FailedValidatorError(PropertyError):
    def __init__(self, key, blockObj:SingleBlock, cause:Exception, *args, blockDict={}, **kwargs):
        
        super().__init__(key, blockObj, *args, blockDict=blockDict, hint="Failed to validate property: ", **kwargs)

        self.cause = cause

        self.__cause__ = cause

class PropertyAliasError(PropertyError):
    def __init__(self, key, blockObj:SingleBlock, *args, blockDict={}, hint="Problem with aliased property: ", posthint:str=None, **kwargs):
        super().__init__(key, blockObj, *args, blockDict=blockDict, hint=hint, **kwargs)
        if posthint is not None:
            self.args[0] += "\n" + posthint

class ListBlockError(Exception):
    def __init__(self, blockObj:ListBlock, *args, hint="Error constructing ListBlock", posthint:str=None, **kwargs):
        self.blockObj = blockObj
        self.typ_nm, _, _ = _get_block_info(blockObj)
        self.hint = hint
        self.posthint = posthint
        self._build_hint()

        super().__init__(self.hint, *args, **kwargs)

    def _build_hint(self):
        self._build_prehint()
        self._build_posthint()

    def _build_prehint(self):
        self.hint += f" ({self.typ_nm} Type)"
    
    def _build_posthint(self):
        self.hint += f":\n{self.posthint}"


class ListBlockMismatchError(ListBlockError):
    def __init__(self, blockObj:ListBlock, candidate, *args, hint="Error adding block to ListBlock:", posthint:str=None, cause:Exception=None, **kwargs):
        self.candidate = candidate


        super().__init__(blockObj, *args, hint=hint, **kwargs)

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

class ListBlockErrorGroup(ExceptionGroup, ListBlockError):
    def __init__(self, blockObj:ListBlock, errors=[]):
        typ_nm, _, _ = _get_block_info(blockObj)
        super().__init__(f"Error(s) occurred when trying to construct or modify '{typ_nm}' object.", errors)
