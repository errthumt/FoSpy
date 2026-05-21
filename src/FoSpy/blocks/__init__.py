"""Classes for representing blocks of information in a FOS file.

Synthesis objects are constructed as a FileBlock subclass, which contain
attributes specified by headers in the file. Each FileBlock attribute
is a subclass object of another block class (either SingleBlock or ListBlock)
ListBlocks wrap a list of SingleBlock objects.
SingleBlock attributes can be assigned to simple values or other blocks.

Typical usage:
```
mySyn = Synthesis.fromFile("C:\\my.fos")

# mySyn.reaction is a SingleBlock object
# mySyn.reaction.nominal_mass is a Decimal value
nom_mass = mySyn.reaction.nominal_mass

# mySyn.materials is a ListBlock object containing SingleBlock Material objects.
zinc = mySyn.materials[0]
print(zinc.formula)
"""

'''
from .blocks import FileBlock, SingleBlock, ListBlock 
from .embedded import *
from .template import *
from .synthesis import *   
from .materials import *
from .metadata import *
from .treatments import *
'''

