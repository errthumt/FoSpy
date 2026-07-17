from FoSpy import FileBlock

synthesis = FileBlock.fromFile(r"C:\Users\travi\FoSpy\mkdocs\docs\examples\synthesis\start_synthesis.fos")
synthesis.package("test_package.fosx")