import ttkbootstrap as tb


class ButtonPanel(tb.Frame): # pylint: disable=too-many-ancestors
    """A navigation panel, containing a button group.

    Parameters
    ----------
    ttk_string_var: ttkbootstrap.StringVar
        The string variable which is to be set by the buttons. The
        variable will be filled with the label of the selected button.
    labels: list(str)
        A list of strings which are to appear on the buttons.
    styling: {padx: int, pady: int, font: (str, int), colors: {text: str, highlight: str}}
    """
    def __init__(
            self,
            parent,
            ttk_string_var,
            labels,
            styling,
            ttk_key_var=None
        ):
        super().__init__(master=parent)

        self.buttons = []
        if isinstance(labels, list):
            for tab in labels:
                self.buttons.append(TextButton(
                    master=self,
                    text=tab,
                    tab_nav_str=ttk_string_var,
                    button_group=self.buttons,
                    styling=styling
                ))
        else:
            for key, value in labels.items():
                self.buttons.append(TextButton(
                    master=self,
                    text=value,
                    tab_nav_str=ttk_string_var,
                    button_group=self.buttons,
                    styling=styling,
                    key=key,
                    tab_nav_int=ttk_key_var
                ))


class TextButton(tb.Label): # pylint: disable=too-many-ancestors
    """
    Parameters
    ----------
    button_group: list(TabTextButton)
        The button group this button belongs to. When the button is
        highlighted, all other buttons of the same group are unselected
        via the unselect() function.
    """
    def __init__(
            self,
            master,
            text,
            tab_nav_str,
            button_group,
            styling,
            key=None,
            tab_nav_int=None
        ):
        self.colors = styling['colors']
        super().__init__(
            master=master,
            text=text,
            foreground=self.colors['text'],
            font=styling['font']
        )
        self.bind('<Button-1>', self.select_handler)

        self.button_group = button_group
        self.key = key
        self.text = text
        self.tab_nav_int = tab_nav_int
        self.tab_nav_str = tab_nav_str

        if tab_nav_str.get() == text:
            self.select_handler()

        self.pack(
            side=styling['side'],
            padx=styling['padx'],
            pady=styling['pady'],
            anchor=styling['anchor']
        )

    def select_handler(self, *_args):
        """Callback method for when the label is clicked on.
        """
        if self.tab_nav_int is not None:
            self.tab_nav_int.set(self.key)
        self.tab_nav_str.set(self.text)
        for button in self.button_group:
            button.unselect()
        self.configure(foreground=self.colors['highlight'])

    def unselect(self):
        """Resets the text color."""
        self.configure(foreground=self.colors['text'])
