#### Additional Requirements

In addition to the required properties above, all `Attachment` objects must be constructed with one of the following optional properties:

- `embedded`
- `path`

The first matching property found will be used and the remainder will be discarded. The presence of one of these properties is used to identify what form of file attachment it is. Refer to the [attachments guide](../guides/attachments.md) for more information

##### Attachment Types

- [`EmbeddedFile` (Embedded text content)](#embeddedfile)
- [`PathFile` (Referenced by relative path)](#pathfile)


##### File Types

- [`CIFFile` (Crystallographic Information File)](#ciffile)


#### Attachment Method Subclasses

Attachment Subclasses are hybridized between an **attachment type** and a **file type**. Attachment types share most method names to be called by *file type* methods, but method source code differs on the basis of how the file was attached. For example, `_get_filepath()` for [`PathFile`](../blocks/attachments.md#FoSpy.blocks.attachments.PathFile._get_filepath) simply returns an absolute filepath resolved from the value in its `path` attribute, whereas [`EmbeddedFile`](../blocks/attachments.md#FoSpy.blocks.attachments.EmbeddedFile._get_filepath) objects create a temporary file to print their embedded lines to before returning its filepath.

Attachment types are dispatched based on which optional properties they have. File types are dispatched based on extension. Unrecognized extensions simply don't add any special file type methods.

