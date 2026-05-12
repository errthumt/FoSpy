class SingleBlock:
    """
    A single key–value block parsed from a FOS file.

    Parameters
    ----------
    blockDict : dict
        Mapping of field names to scalar values. Subclasses perform
        validation and type conversion.
    """
    @classmethod
    def from_listblock(cls, blockDict):
        """
        Optional dispatcher to allow subclass delegation when constructing
        from ListBlock. Overridden in some subclasses
        """
        # Default: construct normally.
        return cls(blockDict)

    def __init__(self, blockDict):
        pass


class ListBlock:
    """
    A repeated‑entry block parsed from a FOS file.

    Each key in `blockDict` maps to a list of equal length. Each list
    index defines one object, constructed by `cls` from a dict of
    key → value pairs at that index.

    Parameters
    ----------
    blockDict : dict
        Mapping of field names to lists of values. All lists must have
        the same length.
    cls : type
        Class used to construct each item. Validation is delegated to `cls`.
    """
    def __init__(self, blockDict, cls):

        # validate that blockDict contains a list of same length
        # under every key
        value_lists = list(blockDict.values())
        if not all(isinstance(v, list) for v in value_lists):
            raise TypeError("All values in blockDict must be lists.")
        

        lengths = {len(v) for v in value_lists}
        if len(lengths) != 1:
            raise ValueError(f"All lists in blockDict must be equal length. Got multiple lengths: {lengths}")

        self.items = []
        for values in zip(*value_lists):
            item_dict = dict(zip(blockDict.keys(), values))
            self.items.append(cls.from_listblock(item_dict))

    def __getitem__(self, idx):
        return self.items[idx]
    
    def __len__(self):
        return len(self.items)
    
    def __iter__(self):
        return iter(self.items)

class Material(SingleBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)

class MaterialList(ListBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict, Material)

class Treatment(SingleBlock):
    # Maps type strings to subclass constructors.
    # Populated in subclass definitions
    dispatch = {}

    @classmethod
    def from_listblock(cls, blockDict):
        t = blockDict.get("type")
        subclass = cls.dispatch.get(t,cls)
        return subclass(blockDict)

    def __init__(self, blockDict):
        super().__init__(blockDict)

class Annealing(Treatment):
    def __init__(self, blockDict):
        super().__init__(blockDict)
Treatment.dispatch["anneal"] = Annealing

class TreamentList(ListBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict, Treatment)

class Data(SingleBlock):
    def __init__(self, blockDict):
        super().__init__(blockDict)