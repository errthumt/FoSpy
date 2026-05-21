def inherit_docstring(parent, label="Parent"):
    def decorator(func):
        parent_doc = getattr(parent, func.__name__).__doc__
        if parent_doc:
            func.__doc__ = (func.__doc__ or "") + f"\n\n{label} doc: `{parent.__name__}.{func.__name__}`\n" + parent_doc
        return func
    return decorator

def attach_doc(source, label="Related"):
    """
    Attach the docstring from `source` to the decorated function or class.

    `source` may be:
        • a function
        • a class
        • any object with a __doc__ attribute
        • a literal string (treated as a docstring)
    """
    # Resolve the docstring
    if isinstance(source, str):
        source_doc = source
        source_name = None
    else:
        source_doc = getattr(source, "__doc__", None)
        source_name = getattr(source, "__qualname__", None)

    def decorator(obj):
        if source_doc:
            header = f"\n\n{label} doc"
            if source_name:
                header += f": `{source_name}`"
            header += "\n"

            obj.__doc__ = (obj.__doc__ or "") + header + source_doc
        return obj

    return decorator


def inherit_class_doc(parent):
    def decorator(cls):
        parent_doc = parent.__doc__
        if parent_doc:
            cls.__doc__ = (cls.__doc__ or "") + f"\n\nParent doc: `{parent.__name__}`\n" + parent_doc
        return cls
    return decorator


from .blocks.blocks import SingleBlock, FileBlock, ListBlock