# Managing FOS files for Your Group

The core spirit of the FOS format is to establish a serialized way of communicating your positive and negative experimental results with other scientists via a database or results package. That being said, the format is also intended to be useful for keeping and indexing your own localized copy of results. Further complication arises when considering that, by default, experimenters will not be uploading results to a public database at the time of generation; even unsuccessful results provide insights into the ongoing work that may not be appropriate to expose before publication. 

<ins>**To reconcile these goals, the following standards are proposed:**</ins>

1. The top-level identifier for a FOS format should be a unique, immutable ID corresponding to the generating research group or organization
2. Within the top-level scope, categorization and metadata can be tailored to the needs of the generating group
3. Lowest-level identification (Experiment ID) should be unique within the scope of the generating group, or, at bare minimum, the tailored category

By following these standards, experimenters are empowered to manage their own localized results however they see fit, while still ensuring that, at the time of *local* generation, results are already equipped with identifiers that won't conflict with a database when the group sees fit to upload. There are many possible ways to achieve this, but the [current FOS validation](../expected/index.md) enforces the recommendations on this page. 

*File management standards may be changed during development; If this occurs, tools will be prepared to bring outdated files back into alignment with current guidelines.*

## Group ID
[Metadata blocks for a synthesis file](../expected/index.md#synthesismeta) are required at read time to contain a `group_id` value. This value is a unique identifier which applies to the parent research group or organization of the generating researcher.

- **<ins>Required:</ins>** The `group_id` key must be present and not empty.
- **<ins>Current Guidelines:</ins>** `group_id` values can be ensured as unique by ending with the primary investigator's ORCID (example: `kovnir-0000-0003-1152-1912`).
- **<ins>Future Intent:</ins>** Unique `group_id` values should be standardized, authenticated, and/or issued by a central party to ensure that all future database uploads have a unique index location.

## Project ID

[Metadata blocks for a synthesis file](../expected/index.md#synthesismeta) are required at read time to contain a `project_id` value. This value is more flexible than `group_id`, in that it can be used for any categorization desired by the group. 

- **<ins>Required:</ins>** The `project_id` key must be present and not empty.
- **<ins>Current Guidelines:</ins>** `project_id` values can use separator characters to mirror a nested file structure. A large experimental group, for example, might categorize syntheses by experimenter then project, or vice versa for intra-collaboration. To avoid conflicts with similar names (present or future), name-based categories should be given unique suffixes, like university ID/username or the last 4 digits of the ORCID. Some examples:
  - `travis5672/clathrates`
  - `travis(errthumt)/pnictides`
  - `thermoelectrics/travis5672/Ba2-TM5-Pn6`
- **<ins>Future Intent:</ins>** [Configuration](./config.md) options or automated tools may be added to automatically maintain group file structure, track individual filepaths for group categories, or rearrange scattered files into a matching group file directory. Databases can index by `project_id` within the parent `group_id`

## FOS ID
[Metadata blocks for *any* file](../expected/index.md#metadata) are required at read time to contain a `fos_id` value.

- **<ins>Required:</ins>** The `fos_id` key must be present and not empty.
- **<ins>Current Guidelines:</ins>** The `fos_id` value should be a unique, brief, descriptive summary of the synthesis. Consider using filename-compatible syntax.
- **<ins>Future Intent:</ins>** `fos_id` values can be considered synonomous with filenames for database storage. [Configuration](./config.md) options may be added to optionally automate or enforce this.