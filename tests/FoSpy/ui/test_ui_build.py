import pytest

class Empty:
    def main_loop(self):
        self._ok_clicked()

@pytest.fixture
def EmptySlider():
    return Empty

def test_matplotlib_ui_build(EmptySlider):
    from FoSpy.ui.sliders.abstract import AssembleSlider

    ui = AssembleSlider(EmptySlider, ui='matplotlib')()
    
    assert ui.main_loop() is None

def test_pyqtgraph_ui_build(EmptySlider):
    from FoSpy.ui.sliders.abstract import AssembleSlider

    ui = AssembleSlider(EmptySlider, ui='pyqtgraph')()
    
    assert ui.main_loop() is None

