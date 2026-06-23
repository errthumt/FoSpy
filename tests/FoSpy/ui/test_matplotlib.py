import pytest

import FoSpy.ui.matplotlib


@pytest.mark.parametrize(
    "slider_width,expected",
    [
        # TODO: fill in test data for test_get_label_offset
        # pytest.param(, id="")
    ]
)
def test_get_label_offset(slider_width, expected):
    # TODO: create assertions for test_get_label_offset
    # FoSpy.ui.matplotlib._get_label_offset(slider_width)
    pass


@pytest.mark.parametrize(
    "parent,expected",
    [
        # TODO: fill in test data for test_hseparator
        # pytest.param(, id="")
    ]
)
def test_hseparator(parent, expected):
    # TODO: create assertions for test_hseparator
    # FoSpy.ui.matplotlib._hseparator(parent)
    pass


@pytest.mark.parametrize(
    "parent,expected",
    [
        # TODO: fill in test data for test_vseparator
        # pytest.param(, id="")
    ]
)
def test_vseparator(parent, expected):
    # TODO: create assertions for test_vseparator
    # FoSpy.ui.matplotlib._vseparator(parent)
    pass


@pytest.mark.parametrize(
    "instance,w,expected",
    [
        # TODO: fill in test data for test_controlpanel_addwidget
        # pytest.param(FoSpy.ui.matplotlib.ControlPanel(rows, parent), , expected, id="")
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
        # pytest.param(FoSpy.ui.matplotlib.ControlPanel(rows, parent), , , expected, id="")
    ]
)
def test_controlpanel_addgroup(instance, label, rows, expected):
    # TODO: write test for test_controlpanel_addgroup
    # TODO: create assertions for test_controlpanel_addgroup
    # instance.addGroup(label, rows)
    pass


@pytest.mark.parametrize(
    "instance,frame,expected",
    [
        # TODO: fill in test data for test_controlpanel_show_group
        # pytest.param(FoSpy.ui.matplotlib.ControlPanel(rows, parent), , expected, id="")
    ]
)
def test_controlpanel_show_group(instance, frame, expected):
    # TODO: write test for test_controlpanel_show_group
    # TODO: create assertions for test_controlpanel_show_group
    # instance._show_group(frame)
    pass


@pytest.mark.parametrize(
    "instance,name,spec,expected",
    [
        # TODO: fill in test data for test_sliderplot_add_scalar
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), , , expected, id="")
    ]
)
def test_sliderplot_add_scalar(instance, name, spec, expected):
    # TODO: write test for test_sliderplot_add_scalar
    # TODO: create assertions for test_sliderplot_add_scalar
    # instance._add_scalar(name, spec)
    pass


@pytest.mark.parametrize(
    "instance,name,digits,expected",
    [
        # TODO: fill in test data for test_sliderplot_slider_changed
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), , , expected, id="")
    ]
)
def test_sliderplot_slider_changed(instance, name, digits, expected):
    # TODO: write test for test_sliderplot_slider_changed
    # TODO: create assertions for test_sliderplot_slider_changed
    # instance.slider_changed(name, digits)
    pass


@pytest.mark.parametrize(
    "instance,name,digits,min_,max_,expected",
    [
        # TODO: fill in test data for test_sliderplot_textbox_changed
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), , , , , expected, id="")
    ]
)
def test_sliderplot_textbox_changed(instance, name, digits, min_, max_, expected):
    # TODO: write test for test_sliderplot_textbox_changed
    # TODO: create assertions for test_sliderplot_textbox_changed
    # instance.textbox_changed(name, digits, min_, max_)
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_sliderplot_ok_clicked
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), expected, id="")
    ]
)
def test_sliderplot_ok_clicked(instance, expected):
    # TODO: write test for test_sliderplot_ok_clicked
    # TODO: create assertions for test_sliderplot_ok_clicked
    # instance._ok_clicked()
    pass


@pytest.mark.parametrize(
    "instance,label,expected",
    [
        # TODO: fill in test data for test_sliderplot_setxlabel
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
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
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
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
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
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
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
    ]
)
def test_sliderplot_setyticks(instance, on, expected):
    # TODO: write test for test_sliderplot_setyticks
    # TODO: create assertions for test_sliderplot_setyticks
    # instance.setYticks(on)
    pass


@pytest.mark.parametrize(
    "instance,spec_name,expected",
    [
        # TODO: fill in test data for test_sliderplot_disable_slider
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
    ]
)
def test_sliderplot_disable_slider(instance, spec_name, expected):
    # TODO: write test for test_sliderplot_disable_slider
    # TODO: create assertions for test_sliderplot_disable_slider
    # instance.disable_slider(spec_name)
    pass


@pytest.mark.parametrize(
    "instance,spec_name,expected",
    [
        # TODO: fill in test data for test_sliderplot_enable_slider
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
    ]
)
def test_sliderplot_enable_slider(instance, spec_name, expected):
    # TODO: write test for test_sliderplot_enable_slider
    # TODO: create assertions for test_sliderplot_enable_slider
    # instance.enable_slider(spec_name)
    pass


@pytest.mark.parametrize(
    "instance,spec_name,expected",
    [
        # TODO: fill in test data for test_sliderplot_toggle_slider
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
    ]
)
def test_sliderplot_toggle_slider(instance, spec_name, expected):
    # TODO: write test for test_sliderplot_toggle_slider
    # TODO: create assertions for test_sliderplot_toggle_slider
    # instance.toggle_slider(spec_name)
    pass


@pytest.mark.parametrize(
    "instance,spec_name,expected",
    [
        # TODO: fill in test data for test_sliderplot_get_slider_val
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
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
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
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
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), expected, id="")
    ]
)
def test_sliderplot_reset_sticks(instance, expected):
    # TODO: write test for test_sliderplot_reset_sticks
    # TODO: create assertions for test_sliderplot_reset_sticks
    # instance.reset_sticks()
    pass


@pytest.mark.parametrize(
    "instance,segments,plotset,expected",
    [
        # TODO: fill in test data for test_sliderplot_add_sticks
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), , , expected, id="")
    ]
)
def test_sliderplot_add_sticks(instance, segments, plotset, expected):
    # TODO: write test for test_sliderplot_add_sticks
    # TODO: create assertions for test_sliderplot_add_sticks
    # instance.add_sticks(segments, plotset)
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_sliderplot_draw_sticks
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), expected, id="")
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
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
    ]
)
def test_sliderplot_plotxy(instance, x, expected):
    # TODO: write test for test_sliderplot_plotxy
    # TODO: create assertions for test_sliderplot_plotxy
    # instance.plotXY(x)
    pass


@pytest.mark.parametrize(
    "instance,x_left,x_right,y,cap_height,plotset,color,expected",
    [
        # TODO: fill in test data for test_sliderplot_draw_width_bracket
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), , , , , , , expected, id="")
    ]
)
def test_sliderplot_draw_width_bracket(instance, x_left, x_right, y, cap_height, plotset, color, expected):
    # TODO: write test for test_sliderplot_draw_width_bracket
    # TODO: create assertions for test_sliderplot_draw_width_bracket
    # instance.draw_width_bracket(x_left, x_right, y, cap_height, plotset, color)
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_sliderplot_reset_plotsets
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), expected, id="")
    ]
)
def test_sliderplot_reset_plotsets(instance, expected):
    # TODO: write test for test_sliderplot_reset_plotsets
    # TODO: create assertions for test_sliderplot_reset_plotsets
    # instance.reset_plotsets()
    pass


@pytest.mark.parametrize(
    "instance,val,expected",
    [
        # TODO: fill in test data for test_sliderplot_update_plot
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), , expected, id="")
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
        # TODO: fill in test data for test_sliderplot_main_loop
        # pytest.param(FoSpy.ui.matplotlib.SliderPlot(figsize, title, specs, cfg, x_label, y_label, x_ticks, y_ticks), expected, id="")
    ]
)
def test_sliderplot_main_loop(instance, expected):
    # TODO: write test for test_sliderplot_main_loop
    # TODO: create assertions for test_sliderplot_main_loop
    # instance.main_loop()
    pass