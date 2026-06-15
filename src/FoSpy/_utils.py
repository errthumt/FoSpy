import math


def _floor_to(x, digits):
    return math.floor(x * 10**digits) / 10**digits


def _ceil_to(x, digits):
    return math.ceil(x * 10**digits) / 10**digits