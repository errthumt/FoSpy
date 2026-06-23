def test_matplotlib_ui_build():
    from FoSpy.ui.abstract import AssembleSlider

    class EmptySlider:
        pass

    ui = AssembleSlider(EmptySlider, ui='matplotlib')()
    
    assert ui.main_loop() == None

