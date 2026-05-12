# Back to the basics: What should the script side of FOS parsing do?

## Parsing Basics:
What should we make sure the script does when reading a FOS file?
* Maintain block order
* Flexible classes for custom data blocks
  * Assign existing classes
  * Allow custom classes? (more complex syntax required)
* Enforce classes for required data blocks
* Look for units when expected.
  * For non-required and required variables
* Embed experimental data
  * Max volume?
* Allow comments within block/data order

## Serializing Basics:
What should we make sure the script does when writing a FOS file?
* Block and comment order from reading should be maintained
* Flexible data types are specified, enforced data types are not (should already be re-enforced when reading)
* Experimental data is preserved (allow compression? How?)

## Class basics:
How do we want to structure the data?
* Synthesis: container class
* Block: `pandas.DataFrame`? Or list of class objects?
  * i.e. should each material be its own object? or should the material list be one object?
* Data: `pandas.DataFrame` stored within any block object.

## Classes:
What "data types" do we want to parse blocks into? What existing data structures can we build these from?

### Synthesis (file level)
A glorified dictionary

<ins>Desired functionality</ins>
* Somehow maintain link between comments and their corresponding blocks.
  * Store comments inside blocks? Maintain block:comments dict?
* Maintain order of blocks
* Enforce required blocks and their types on `__init__`
* Extra values calculated on serialization, added as comments

<ins>Attributes</ins> (variables)
* Metadata
* `sourceFile`
* Comments
* Blocks

<ins>Methods</ins>
* `__init__(self, filepath)`
* `insert_material, insert_treatment, etc.`
* serializer
  * Converts class structure into simple python structure for printing (probably `dict`)
* `save(self, filepath=self.sourceFile)`
  * uses serializer, then prints to file path. Can be used for save or save as

### Experimenters (Synthesis > metadata > experimenters)
Categorize information about experimenters involved

### Generic Block (Synthesis > blocks > any block)
Parent class used for validation of any block type, including custom types.

<ins>Desired functionality</ins>
* Enforce classes required by given subclass
* Edit items within block
* Insert/add items.

<ins>Attributes</ins> (variables)


<ins>Methods</ins>


### Materials

<ins>Desired functionality</ins>

<ins>Attributes</ins> (variables)

<ins>Methods</ins>

### Treatments (synthesis steps)
Can be applied to materials or to main synthesis

<ins>Desired functionality</ins>

<ins>Attributes</ins> (variables)

<ins>Methods</ins>

### Annealing Profiles (treatment subclass)

<ins>Desired functionality</ins>

<ins>Attributes</ins> (variables)

<ins>Methods</ins>


### Experimental Data
Internal `data` class contains x/y/z data, but other metadata should be contained here too, like type or instrument

<ins>Desired functionality</ins>

<ins>Attributes</ins> (variables)

<ins>Methods</ins>
