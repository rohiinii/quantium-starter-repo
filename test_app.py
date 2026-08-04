"""
Test suite for the Pink Morsel sales visualiser Dash app.
Verifies the header, chart, and region picker all render correctly.
"""
from dash.testing.application_runners import import_app


def test_header_is_present(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)

    dash_duo.wait_for_element("h1", timeout=50)
    header = dash_duo.find_element("h1")

    assert "Pink Morsel Sales Visualiser" in header.text


def test_visualisation_is_present(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)

    dash_duo.wait_for_element("#sales-line-chart", timeout=50)
    chart = dash_duo.find_element("#sales-line-chart")

    assert chart is not None


def test_region_picker_is_present(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)

    dash_duo.wait_for_element("#region-filter", timeout=50)
    region_picker = dash_duo.find_element("#region-filter")

    assert region_picker is not None