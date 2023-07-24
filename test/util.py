"""Helper classes for testing a tkinter GUI application.

Methods
-------
_widgets_by_name : Iterates recoursively through the application and
    compares their name to the searched string.
find_widget_by_name : Returns a widget with a specified name from the
    application.
"""


def _widgets_by_name(parent, name, widgets):
    """Traverses the widget tree leaves in search for the specified
    name.

    Parameters
    ----------
    parent
        The tkinter widget to be checked for children (continues to
        traverse) of their name.
    name : str
        The widget name to search for.
    widgets : list
        A reference to a list to store found widgets in.
    """
    if not parent.winfo_children():
        if name == parent.winfo_name():
            widgets.append(parent)
    else:
        for child in parent.winfo_children():
            _widgets_by_name(child, name, widgets)

def find_widget_by_name(parent, name):
    """Searches for tkinter widgets by their respective name. Does not
    search for named frames!

    Parameters
    ----------
    parent
        The tkinter widget from which to start the search from.
    name : str
        The name of the widget to search for.
    """
    widgets = []
    _widgets_by_name(parent, name, widgets)
    if len(widgets) == 0:
        raise ValueError(f"No widget named {name} found.")
    elif len(widgets) > 1:
        raise ValueError(f"Multiple widgets with name {name} found.")
    return widgets[0]
