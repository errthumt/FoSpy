# Attaching Files to the FOS Format

Non-FOS files can be attached to a FOS in a number of different ways. Attached files are tracked by the [`FileBlock`][blockdocs-FileBlock] they are contained within, and maintained in a way that they can be read and written to by commands within the `FoSpy` API or other imported packages.

The class for an attached file is a hybridized subclass of an [attachment type](#attachment-types) and a [file type](#file-types) subclass. The **attachment type** provides the context methods for accessing and modifying the attached file, whereas the **file type** provides methods unique to that file extension (like plotting a CSV or theoretical pattern from a CIF).

## Attachment Types

After validating for [required keys](../expected/index.md#attachment), the method of attachment for any given file is specified by the presence of an expected key. Once a matching key is found, any other "attachment type" keys are rejected as "redundant", and the attachment type is dispatched as one of the following:

| Expected Key | Attachment Type |
| --- | --- |
| `embedded` | [`EmbeddedFile`](#embedded-files) |
| `path` | [`PathFile`](#path-files) |

### Embedded Files

Expected property: `embedded` | Class: [`EmbeddedFile`][blockdocs-EmbeddedFile]

The `embedded` property of an embedded file contains a list of raw lines of utf-8 formatted text read directly from the FOS format. An example for the synax of this can be found in the CIF attached to the [initial synthesis file](../examples/synthesis/index.md#initial-synthesis-fos) in the API example.

When [`_get_filepath()`](../blocks/attachments.md#FoSpy.blocks.attachments.EmbeddedFile._get_filepath) is called for the first time, embedded files obtain a temporary directory path from their containing `FileBlock` and copy the embedded lines to a file at that path. Any future calls to `_get_filepath()` return the written location. Temporary directories are cleaned up and removed by `FileBlock`s at the end of runtime.

### Path Files

Expected property: `path` | Class: [`PathFile`][blockdocs-PathFile]

The `path` property of a path file contains a folder location relative to the `FileBlock` input file (the JSON or FOS-formatted file) See the CIF attached to the [initial templates file](../examples/templates/index.md#initial-templates-fos) for an example.

- The `path` property can use "`.`" to refer to the same folder as the `FileBlock`, or use "`..`" characters to navigate upward in relative filepaths. Refer to the [synthesis file after API checkpoint 9](../examples/synthesis/index.md#checkpoint-9) for one example.

#### Path Examples

For a synthesis file at `C://foo/my_synthesis.fos`:
```fos
[Cif]
file_name: my_structure
extension: .cif

// refers to C://foo/my_structure.cif
path: .

// refers to C://my_structure.cif
path: ..

// refers to C://hello/world/my_structure.cif
path: ../hello/world

// refers to C://foo/bar/my_structure.cif
path: ./bar
```

By default, attached path files will track their original location and update their relative path when transferred to another `FileBlock`. `FileBlock`s also have a method, [`track_attachments`](../blocks/blocks.md#FoSpy.blocks.blocks.Block.track_attachments), that allows some configuration on path tracking behavior:

```python
# keep attached files in their original location and 
# update "path" to match whenever saved or refreshed.
my_synthesis.track_attachments(new_copy=False)

# create new copy in new location whenever saved or refreshed.
# If file already exists, do not overwrite; 
# interpret existing file as new attachment
my_synthesis.track_attachments(new_copy=True, overwrite=False)

# create new copy, but ask user for confirmation if file already exists.
my_synthesis.track_attachments(new_copy=True, overwrite="prompt")
```

Refer to the full `track_attachments` documentation for more guidance.

## File Types

File types are dispatched based on the `extension` value. For niche applications, it is possible to add your own filetype during runtime by creating an `Attachment` subclass and mutating [Attachment.extensions](../blocks/attachments.md#FoSpy.blocks.attachments.Attachment.extensions). However, if you anticipate other scientists using the same filetype, you should [reach out to devs](https://github.com/errthumt/FoSpy/issues/) about incorporating it into the main package.

### CIF Files

Extension: `.cif` | Class: [`CIFFile`][blockdocs-CIFFile]

**(In Progress)**
The `_get_filepath()` method can be used to get the location of the CIF file, and then that location can be passed as a file to any other package intended for reading CIF, such as [pymatgen](https://pypi.org/project/pymatgen/) or [PyCifRW](https://pypi.org/project/PyCifRW/).

Right now, CIF objects are equipped for some very basic plot generation methods. See the class documentation for more information.