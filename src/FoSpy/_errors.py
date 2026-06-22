class AttachmentTypeError(Exception):
    pass


class FileBlockNotFoundError(Exception):
    pass

class PropertyError(Exception):
    pass


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


class MissingPropertyError(ValueError, PropertyError):
    def __init__(self, key, blockObj, blockDict={}, *args, **kwargs):
        typ_nm, block_id, id_key = _get_block_info(blockObj, blockDict)

        hint = f"Missing required property '{key}' for '{typ_nm}' object."

        if block_id is not None:
            hint += f" (ID: {id_key} = {block_id})"

        super().__init__(hint, *args, **kwargs)

class FailedValidatorError(PropertyError):
    def __init__(self, key, blockObj, cause:Exception, blockDict={}, *args, **kwargs):
        typ_nm, block_id, id_key = _get_block_info(blockObj, blockDict)

        hint = f"Failed to validate property '{key}' for '{typ_nm}' object."

        if block_id is not None:
            hint += f" (ID: {id_key} = {block_id})"

        super().__init__(hint, *args, **kwargs)
        self.__cause__ = cause
        self.cause = cause