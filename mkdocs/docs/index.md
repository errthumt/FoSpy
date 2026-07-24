# FoSpy
A framework for opening, editing, and saving Files of Synthesis (*.fos)

The File of Synthesis project is an effort from [Kovnir Group at Iowa State](https://group.chem.iastate.edu/Kovnir/index.html) to establish a standardized, machine-readable format for communicating synthetic methods *and outcomes* for materials and solid-state chemistry. Access to data on negative experimental outcomes is becoming increasingly important for predicting new materials and the methods required to obtain them. **Quick and easy file generation for *failed* experiments is a core objective for the project**, and we hope that establishing the FoS format as a form of electronic notebook (ELN) utility will simplify the steps to get results from the benchtop to the public, regardless of their success.

## New GUI
There is now a GUI application for interacting with the FoS format! Setup is easy with an existing Python >= 3.11 environment. 

```bash
$ pip install FoSpy[app]
$ fospy-app
```

**It is recommended to install FoSpy in its [own virtual environment](https://docs.python.org/3/library/venv.html).** Refer to the [getting started](guides/getting_started.md) guide for more information.

Currently, only fully-validated files (meeting all requirements set forth by the [expected properties](expected/index.md) page) are able to be opened by the app, but we are working on features for opening an incomplete file as a fillable template. For now, there are a few example files packaged in the app menu, or you can refer to examples from the old [code example](examples/code_example/index.md).

## Survey: Try Making Your Own FOS

We are looking for as much input as possible from other scientists about what types of information should be in the FOS format. Create your own file of synthesis that precisely describes your synthetic approach to a material. **Don't worry about strict syntax guidelines or how long it might take to make these files in bulk** (GUI and LLM automation are right around the corner). Only worry about capturing all the relevant information so that we can make sure our format standards will work for you.

The FOS format is intended to communicate unsuccessful results just as much as successful ones. Consider submitting examples where the synthesis didn't go well, and what techniques you used to make that determination.

You can try opening and editing an existing file in the new GUI, or manually typing details. Again, don't concern yourself as much with syntax. We are more interested in making sure that FoS standards can be followed consistently.

1. Check out some [example synthesis files](./examples/synthesis/index.md)
2. Download [the empty FOS File](./file_download/empty_fos.fos)
3. Add details about your synthesis
   1. If possible include notes about what characterization techniques, software, filetypes, etc. were used.
   2. Don't include any cutting edge or sensitive information in the file; Some submissions will be available on the public-facing GitHub.
   3. Edit and save the file as a `.txt` file to skip security filters.
4. Attach the file to a [Github Issue](https://www.github.com/errthumt/FoSpy/issues/new) or email to [errthumt@iastate.edu](mailto:errthumt@iastate.edu)

## Grammar Extension for IDE (TextMate)
[VSCode Grammar Extension for FOS Files](https://github.com/errthumt/fos-grammar)

The standalone TextMate JSON can also be found in the extension files.

