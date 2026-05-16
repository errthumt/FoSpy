def inherit_docstring(parent):
    def decorator(func):
        parent_doc = getattr(parent, func.__name__).__doc__
        if parent_doc:
            func.__doc__ = (func.__doc__ or "") + "\n\nParent doc:\n" + parent_doc
        return func
    return decorator

def inherit_class_doc(parent):
    def decorator(cls):
        parent_doc = parent.__doc__
        if parent_doc:
            cls.__doc__ = (cls.__doc__ or "") + "\n\nParent doc:\n" + parent_doc
        return cls
    return decorator


from FoSpy.blocks import *
from FoSpy.parsing import *