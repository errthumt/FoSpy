from .chemicals import Chemical
from .blocks import ListBlock


class Product(Chemical):
    pass

ProductList = ListBlock.Simple(Product)
"""
A [simple list][FoSpy.blocks.blocks.ListBlock.Simple] of
[`Product` objects][FoSpy.blocks.products.Product].
"""