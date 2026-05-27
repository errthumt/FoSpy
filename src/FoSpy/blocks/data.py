from .blocks import SingleBlock


class TraceData(SingleBlock):
    pass

class CSVdata(SingleBlock):
    @classmethod
    def fromFile(cls, file):
        pass

    def __init__(self, pointList):
        if not isinstance(pointList, list):
            raise TypeError("CSVdata must be constructed from a list of point dictionaries")
        
        def checkMode(current, new):
            if current is None:
                return new
            elif current != new:
                raise ValueError("You cannot mix comma-separated and separate point dictionaries in the same CSVdata object")
            else:
                return current
        
        points = None
        readMode = None
        for point in pointList:
            if not isinstance(point, dict):
                raise TypeError("CSVdata must be constructed from a list of point dictionaries")
            
            keys = list(point.keys())
            if len(keys) != 1:
                readMode = checkMode(readMode, "separate")
            
            else:
                if "," in keys[0]:
                    readMode = checkMode(readMode, "commas")
                else:
                    readMode = checkMode(readMode, "separate")

            if readMode == "commas":
                keys = [k.strip() for k in keys[0].split(",")]
                points = [v.strip() for v in point[keys[0]].split(" ")]
                if points is None:
                    points = {k: [v] for k, v in zip(keys, points)}
                    continue
                else:
                    if keys != list(points.keys()):
                        raise ValueError("All CSV points must have the same keys")
                    if len(points) != len(keys):
                        raise ValueError("All CSV points must have the same number of values")
                    
                    for k, v in zip(keys, points):
                        points[k].append(v)
            else:
                if any("," in k for k in keys):
                    raise ValueError("You cannot mix comma-separated and separate point dictionaries in the same CSVdata object")
                if points is None:
                    points = {k: [v] for k, v in point.items()}
                    continue
                else:
                    if keys != list(points.keys()):
                        raise ValueError("All CSV points must have the same keys")
                    for k, v in point.items():
                        points[k].append(v)

        super().dispatch_subclass(blockDict=points)

    def __setattr__(self, name, value):
        from ..parsing.validation import optional_keys
        optional_keys.setdefault(self.__class__, {})
        optional_keys[self.__class__][name] = list
