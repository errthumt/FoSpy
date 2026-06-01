# UW-Madison Solid State and Materials Chemistry Collaboration Incubator 2026
I was fortunate enough to attend the [SSMC-CI at UW-Madison](https://ssmcci.chem.wisc.edu/about/) in May 2026, where I connected with new collaborators and gave other researchers their first looks at the proposed "File of Synthesis" format.

The SSMC-CI event is focused on ingesting applicants' individual proposed projects and connecting them with collaborators that might contribute to a larger-scoped project centering on material science and information technology. With the guidance of SSMC-CI organizers, we laid down the groundwork for a collaboration focused on filling in the gap of "negative data" missing from published results used to train machine learning models.

*The lack of publicly available results for unsuccessful syntheses introduces a bias that must be accounted for with approaches such as positive-unlabeled datasets. These methods may offset the effect, but any amount of data for failed or unexpected syntheses could drastically reduce "false positive" predictions for new materials or synthetic techniques. A significant barrier to making unsuccessful results available is the amount of time it takes for an experimenter to format and describe their results, with little to no return on their investment (no papers for unsuccessful syntheses).*

Our group chose to focus on reducing the time and effort required to communicate negative results in a succinct, informational format. We approached the problem from several angles and integrated our own backgrounds and projects whenever possible. SSMC-CI encourages a high level of cross-table communication, so in addition to the collaborators below, we got lots of great input from other researchers who were excited and interested in the project.

| Collaborators | Links | Project contributions<br>*Not Exhaustive* |
| --- | --- | --- |
| Travis Errthum | [Kovnir Group @ Iowa State](https://group.chem.iastate.edu/Kovnir/)<br>[ORCID](https://orcid.org/0009-0006-1937-5672) | FOS format and API for standardized reporting of syntheses |
| Zach Zheng &<br>Peter Walther | [Zheng Group @ WashU St. Louis](https://zhenglab.wustl.edu/)<br>[Google Scholar](https://scholar.google.com/citations?user=02kSQ3IAAAAJ) | Training LLMs to serialize synthetic methods and results from various input methods, including audio recordings and handwritten notebook entries. |
Jill Wenderott | [Wenderott Group @ Drexel](https://drexel.edu/engineering/about/faculty-staff/W/wenderott-jill/)<br>[Google Scholar](https://scholar.google.com/citations?user=XjI8ZOMAAAAJ&hl=en) | Integrating the standardized format into their existing workflow for generating electronic notebook entries from laboratory video footage. |
Jeff Rinehart | [Rinehart Group @ UCSanDiego](https://rinehartgroup.ucsd.edu/research)<br>[Google Scholar](https://scholar.google.com/citations?user=7QscRicAAAAJ&hl=en) | Mapping connections between methods, observations, and results of multiple syntheses for deeper analysis of synthetic outcomes. |

**<ins>Some of the significant progress made on the `FoSpy` project as a result of this event:</ins>**
* Further input on what kind of information should be required or expected for synthesis files.
* A formalized and flexible strategy for mapping electronic notebook entries from any JSON structure into the standardized file structure via `FoSpy.json.utils`.
* More rigorous treatment of validation and calculations with units.
* Proof-of-concept for training LLM's to fill in synthesis files using a serialized description of required fields.
  * This may be imrpoved in the future to use [`FoSpy` documentation](../docs/required_properties/index.md) as a source of truth.
* Discussion and first steps for how to include characterization and synthetic outcomes in a synthesis file.

The in-person portion of SSMC-CI ends with a 15-minute presentation from each group on their progress. A copy of our slides can be found [here](./Final_Presentation.pptx)



