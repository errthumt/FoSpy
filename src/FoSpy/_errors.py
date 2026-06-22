class AttachmentTypeError(Exception):
    pass


class FileBlockNotFoundError(Exception):
    pass

class PropertyError(Exception):
    def __init__(self, key, blockObj, blockDict={}, hint="Error for property: ", *args, **kwargs):
        typ_nm, block_id, id_key = _get_block_info(blockObj, blockDict)

        hint += f"'{key}' for '{typ_nm}' object."
        if block_id is not None:
            hint += f" (ID: {id_key} = {block_id})"

        super().__init__(hint, *args, **kwargs)


def _get_block_info(blockObj, blockDict={}):
    typ = type(blockObj)
    typ_nm = typ.__name__

    if hasattr(typ, "id_key"):
        id_key = typ.id_key
        block_id = blockDict.get(id_key, None)
    else:
        block_id = None

    return typ_nm, block_id, id_key

class PropertyErrorGroup(ExceptionGroup, PropertyError):
    def __init__(self, blockObj, blockDict={}, errors=[]):
        typ_nm, block_id, id_key = _get_block_info(blockObj, blockDict)

        hint = f"Property Error(s) occurred when trying to construct '{typ_nm}' object."

        if block_id is not None:
            hint += f" (ID: {id_key} = {block_id})"

        super().__init__(hint, errors)



class MissingPropertyError(PropertyError):
    def __init__(self, key, blockObj, blockDict={}, *args, **kwargs):
        super().__init__(key, blockObj, blockDict, hint="Missing required property: ", *args, **kwargs)

class FailedValidatorError(PropertyError):
    def __init__(self, key, blockObj, cause:Exception, blockDict={}, *args, **kwargs):
        super().__init__(key, blockObj, blockDict, hint="Failed to validate property: ", *args, **kwargs)

        self.cause = cause

        self.__cause__ = cause

class PropertyAliasError(PropertyError):
    def __init__(self, key, blockObj, blockDict={}, hint="Problem with aliased property: ", posthint:str=None, *args, **kwargs):
        super().__init__(key, blockObj, blockDict, hint, *args, **kwargs)
        if posthint is not None:
            self.args[0] += "\n" + posthint