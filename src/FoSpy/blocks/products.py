from .chemicals import Chemical
from .blocks import ListBlock


class Product(Chemical):
    _id_key = "name"
    pass

ProductList = ListBlock.Simple(Product)
"""
A [simple list][FoSpy.blocks.blocks.ListBlock.Simple] of
[`Product` objects][FoSpy.blocks.products.Product].
"""