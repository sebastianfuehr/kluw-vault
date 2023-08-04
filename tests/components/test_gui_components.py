"""Tests for the MainFrame component."""

from tests.util import find_widget_by_name

import pytest

from app import App
from src.model.orm_base import DBConnection


@pytest.fixture(scope="module")
def app():
    db_connection = DBConnection("/test.db")
    return App(db_connection)


@pytest.mark.parametrize(
    "widget_name, variable_value",
    [
        ("time entries", "Time Entries"),
        ("projects", "Projects"),
        ("categories", "Categories"),
    ],
)
def test_main_frame_tab_navigation(app, widget_name, variable_value):
    """
    Parameters
    ----------
    app : tkinter.Window
    widget_name : str
        The name of the navigation label widget, which should be
        triggered and tested.
    variable_value : tkinter.StringVar
        The tkiner variable which's value should have changed.
    """
    find_widget_by_name(app, widget_name).event_generate("<Button-1>")
    app.update()
    assert app.main_frame.tab_nav_str.get() == variable_value


@pytest.mark.parametrize(
    "widget_names, expected_result",
    [
        (("projects", "test project"), "Test Project"),
        (("categories", "test category"), "Test Category"),
    ],
)
def test_list_frame_navigation(app, widget_names, expected_result):
    """
    Parameters
    ----------
    widget_names : (str, str)
        The first element is the main frame tab to open, the second
        string represents the list frame element.
    expected_result : str
        The variable value set via the ListFrame.
    """
    find_widget_by_name(app, widget_names[0]).event_generate("<Button-1>")
    app.update()
    find_widget_by_name(app, widget_names[1]).event_generate("<Button-1>")
    app.update()
    assert app.main_frame.central_frame.item_str_var.get() == expected_result
