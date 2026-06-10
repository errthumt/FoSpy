from FoSpy._dev.testing import ui

if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(__file__))
    os.chdir("../../dev_build/windows/program_files")

    from FoSpy._dev.testing import _utils
    _utils.REPO_PATH = os.path.abspath("../../../..")
    print(_utils.REPO_PATH)

    ui.get_test(open_result=True)
    pass