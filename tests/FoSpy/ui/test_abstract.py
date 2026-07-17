import pytest

import FoSpy.ui.sliders.abstract


@pytest.mark.parametrize(
    "specs,expected",
    [
        # TODO: fill in test data for test_count_sliders
        # pytest.param(, id="")
    ]
)
def test_count_sliders(specs, expected):
    # TODO: create assertions for test_count_sliders
    # FoSpy.ui.abstract._count_sliders(specs)
    pass


@pytest.mark.parametrize(
    "subcls,ui,expected",
    [
        # TODO: fill in test data for test_AssembleSlider
        # pytest.param(, , id="")
    ]
)
def test_AssembleSlider(subcls, ui, expected):
    # TODO: create assertions for test_AssembleSlider
    # FoSpy.ui.abstract.AssembleSlider(subcls, ui)
    pass


@pytest.mark.parametrize(
    "instance,w,expected",
    [
        # TODO: fill in test data for test_controlpanel_addwidget
        # pytest.param(FoSpy.ui.abstract.ControlPanel(rows), , expected, id="")
    ]
)
def test_controlpanel_addwidget(instance, w, expected):
    # TODO: write test for test_controlpanel_addwidget
    # TODO: create assertions for test_controlpanel_addwidget
    # instance.addWidget(w)
    pass


@pytest.mark.parametrize(
    "instance,label,rows,expected",
    [
        # TODO: fill in test data for test_controlpanel_addgroup
        # pytest.param(FoSpy.ui.abstract.ControlPanel(rows), , , expected, id="")
    ]
)
def test_controlpanel_addgroup(instance, label, rows, expected):
    # TODO: write test for test_controlpanel_addgroup
    # TODO: create assertions for test_controlpanel_addgroup
    # instance.addGroup(label, rows)
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_controlpanel_row_col_iter
        # pytest.param(FoSpy.ui.abstract.ControlPanel(rows), expected, id="")
    ]
)
def test_controlpanel_row_col_iter(instance, expected):
    # TODO: write test for test_controlpanel_row_col_iter
    # TODO: create assertions for test_controlpanel_row_col_iter
    # instance.row_col_iter()
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_controlpanel_nextrowcol
        # pytest.param(FoSpy.ui.abstract.ControlPanel(rows), expected, id="")
    ]
)
def test_controlpanel_nextrowcol(instance, expected):
    # TODO: write test for test_controlpanel_nextrowcol
    # TODO: create assertions for test_controlpanel_nextrowcol
    # instance.nextRowCol()
    pass


@pytest.mark.parametrize(
    "instance,specs,expected",
    [
        # TODO: fill in test data for test_sliderplot_unpack_specs
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
    ]
)
def test_sliderplot_unpack_specs(instance, specs, expected):
    # TODO: write test for test_sliderplot_unpack_specs
    # TODO: create assertions for test_sliderplot_unpack_specs
    # instance._unpack_specs(specs)
    pass


@pytest.mark.parametrize(
    "instance,val,expected",
    [
        # TODO: fill in test data for test_sliderplot_update_plot
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
    ]
)
def test_sliderplot_update_plot(instance, val, expected):
    # TODO: write test for test_sliderplot_update_plot
    # TODO: create assertions for test_sliderplot_update_plot
    # instance.update_plot(val)
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_sliderplot_update_cfg
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), expected, id="")
    ]
)
def test_sliderplot_update_cfg(instance, expected):
    # TODO: write test for test_sliderplot_update_cfg
    # TODO: create assertions for test_sliderplot_update_cfg
    # instance.update_cfg()
    pass


@pytest.mark.parametrize(
    "instance,label,specs,rows,expected",
    [
        # TODO: fill in test data for test_sliderplot_add_group
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), , , , expected, id="")
    ]
)
def test_sliderplot_add_group(instance, label, specs, rows, expected):
    # TODO: write test for test_sliderplot_add_group
    # TODO: create assertions for test_sliderplot_add_group
    # instance._add_group(label, specs, rows)
    pass


@pytest.mark.parametrize(
    "instance,name,spec,expected",
    [
        # TODO: fill in test data for test_sliderplot_add_range
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), , , expected, id="")
    ]
)
def test_sliderplot_add_range(instance, name, spec, expected):
    # TODO: write test for test_sliderplot_add_range
    # TODO: create assertions for test_sliderplot_add_range
    # instance._add_range(name, spec)
    pass


@pytest.mark.parametrize(
    "instance,specs,expected",
    [
        # TODO: fill in test data for test_sliderplot_build_controls
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
    ]
)
def test_sliderplot_build_controls(instance, specs, expected):
    # TODO: write test for test_sliderplot_build_controls
    # TODO: create assertions for test_sliderplot_build_controls
    # instance._build_controls(specs)
    pass


@pytest.mark.parametrize(
    "instance,name,spec,expected",
    [
        # TODO: fill in test data for test_sliderplot_add_scalar
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), , , expected, id="")
    ]
)
def test_sliderplot_add_scalar(instance, name, spec, expected):
    # TODO: write test for test_sliderplot_add_scalar
    # TODO: create assertions for test_sliderplot_add_scalar
    # instance._add_scalar(name, spec)
    pass


@pytest.mark.parametrize(
    "instance,spec_name,expected",
    [
        # TODO: fill in test data for test_sliderplot_get_slider_val
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
    ]
)
def test_sliderplot_get_slider_val(instance, spec_name, expected):
    # TODO: write test for test_sliderplot_get_slider_val
    # TODO: create assertions for test_sliderplot_get_slider_val
    # instance.get_slider_val(spec_name)
    pass


@pytest.mark.parametrize(
    "instance,spec_name,expected",
    [
        # TODO: fill in test data for test_sliderplot_get_check_enabled
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
    ]
)
def test_sliderplot_get_check_enabled(instance, spec_name, expected):
    # TODO: write test for test_sliderplot_get_check_enabled
    # TODO: create assertions for test_sliderplot_get_check_enabled
    # instance.get_check_enabled(spec_name)
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_sliderplot_reset_sticks
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), expected, id="")
    ]
)
def test_sliderplot_reset_sticks(instance, expected):
    # TODO: write test for test_sliderplot_reset_sticks
    # TODO: create assertions for test_sliderplot_reset_sticks
    # instance.reset_sticks()
    pass


@pytest.mark.parametrize(
    "instance,segments,expected",
    [
        # TODO: fill in test data for test_sliderplot_add_sticks
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
    ]
)
def test_sliderplot_add_sticks(instance, segments, expected):
    # TODO: write test for test_sliderplot_add_sticks
    # TODO: create assertions for test_sliderplot_add_sticks
    # instance.add_sticks(segments)
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_sliderplot_draw_sticks
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), expected, id="")
    ]
)
def test_sliderplot_draw_sticks(instance, expected):
    # TODO: write test for test_sliderplot_draw_sticks
    # TODO: create assertions for test_sliderplot_draw_sticks
    # instance.draw_sticks()
    pass


@pytest.mark.parametrize(
    "instance,x,expected",
    [
        # TODO: fill in test data for test_sliderplot_plotxy
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
    ]
)
def test_sliderplot_plotxy(instance, x, expected):
    # TODO: write test for test_sliderplot_plotxy
    # TODO: create assertions for test_sliderplot_plotxy
    # instance.plotXY(x)
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_sliderplot_reset_plotsets
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), expected, id="")
    ]
)
def test_sliderplot_reset_plotsets(instance, expected):
    # TODO: write test for test_sliderplot_reset_plotsets
    # TODO: create assertions for test_sliderplot_reset_plotsets
    # instance.reset_plotsets()
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_sliderplot_main_loop
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), expected, id="")
    ]
)
def test_sliderplot_main_loop(instance, expected):
    # TODO: write test for test_sliderplot_main_loop
    # TODO: create assertions for test_sliderplot_main_loop
    # instance.main_loop()
    pass


@pytest.mark.parametrize(
    "instance,label,expected",
    [
        # TODO: fill in test data for test_sliderplot_setxlabel
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
    ]
)
def test_sliderplot_setxlabel(instance, label, expected):
    # TODO: write test for test_sliderplot_setxlabel
    # TODO: create assertions for test_sliderplot_setxlabel
    # instance.setXlabel(label)
    pass


@pytest.mark.parametrize(
    "instance,label,expected",
    [
        # TODO: fill in test data for test_sliderplot_setylabel
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
    ]
)
def test_sliderplot_setylabel(instance, label, expected):
    # TODO: write test for test_sliderplot_setylabel
    # TODO: create assertions for test_sliderplot_setylabel
    # instance.setYlabel(label)
    pass


@pytest.mark.parametrize(
    "instance,on,expected",
    [
        # TODO: fill in test data for test_sliderplot_setxticks
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
    ]
)
def test_sliderplot_setxticks(instance, on, expected):
    # TODO: write test for test_sliderplot_setxticks
    # TODO: create assertions for test_sliderplot_setxticks
    # instance.setXticks(on)
    pass


@pytest.mark.parametrize(
    "instance,on,expected",
    [
        # TODO: fill in test data for test_sliderplot_setyticks
        # pytest.param(FoSpy.ui.abstract.SliderPlot(specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
    ]
)
def test_sliderplot_setyticks(instance, on, expected):
    # TODO: write test for test_sliderplot_setyticks
    # TODO: create assertions for test_sliderplot_setyticks
    # instance.setYticks(on)
    pass