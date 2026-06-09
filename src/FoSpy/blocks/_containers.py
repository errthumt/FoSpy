class SimpleWrapper:
    """
    Wrapper for attaching methods and attributes to simple data types that don't
    support it. Most method or attribute calls are passed through to the wrapped
    value, but some methods or private attributes are attached when setting a
    `SimpleWrapper` as attribute for a `SingleBlock` or `ListBlock`.
    """
    def __init__(self, value):
        self._value = value

    def __iter__(self):
        return self._value.__iter__()

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return repr(self._value)

    def __eq__(self, other):
        return self._value == other

    def __call__(self):
        return self._value

    def __getattr__(self, name):
        return getattr(self._value, name)

    def __getitem__(self, key):
        return self._value.__getitem__(key)

    def __setitem__(self, key, val):
        return self._value.__setitem__(key, val)

    def __int__(self):
        return int(self._value)

    def __float__(self):
        return float(self._value)


class SubContainer:
    """
    A simple container for storing hidden or unexpected attributes of a
    `SingleBlock`

    Values are only assigned directly to `SingleBlock` attributes if they are an
    expected property. Otherwise they are assigned to a `SubContainer` at
    `SingleBlock.ext`. Also used for `SingleBlock._meta`.

    Example Usage:
    ```
    class SingleBlock:
        ... 
        def __setattr__(self, name, value):
            ... 
            if name not in expected:
                return setattr(self.ext, name, value)
    ```
    """
    def __init__(self):
        pass
    def __iter__(self):
        return iter(self.__dict__)