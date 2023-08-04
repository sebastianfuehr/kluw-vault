"""Module which provides elements for navigating through the
application's components.
"""

import ttkbootstrap as tb


class ButtonPanel(tb.Frame):  # pylint: disable=too-many-ancestors
    """A navigation panel, containing a button group.

    Parameters
    ----------
    ttk_string_var : ttkbootstrap.StringVar
        The string variable which is to be set by the buttons. The
        variable will be filled with the label of the selected button.
    labels : list(str) or dict{int: str}
        A list of strings which are to appear on the buttons. If a
        dictionary with key-value pairs is given, also expect a
        ttk_key_var which will be linked to the selected entry text.
    styling : {padx: int, pady: int, font: (str, int), colors:
              {text: str, highlight: str}}
    ttk_key_var : ttkbootstrap.IntVar
        The variable to be set when an entry from the labels dictionary
        is selected.
    context_menu : ContextMenu
    """

    def __init__(
        self,
        parent,
        ttk_string_var,
        labels,
        styling,
        ttk_key_var=None,
        context_menu=None,
        **kwargs
    ) -> None:
        super().__init__(master=parent, **kwargs)

        self.buttons = []
        if isinstance(labels, list):
            for tab in labels:
                self.buttons.append(
                    TextButton(
                        master=self,
                        text=tab,
                        tab_nav_str=ttk_string_var,
                        button_group=self.buttons,
                        styling=styling,
                        context_menu=context_menu,
                    )
                )
        else:
            for key, value in labels.items():
                self.buttons.append(
                    TextButton(
                        master=self,
                        text=value,
                        tab_nav_str=ttk_string_var,
                        button_group=self.buttons,
                        styling=styling,
                        key=key,
                        tab_nav_int=ttk_key_var,
                        context_menu=context_menu,
                    )
                )


class TextButton(tb.Label):  # pylint: disable=too-many-ancestors
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
        tab_nav_int=None,
        context_menu=None,
    ) -> None:
        self.colors = styling["colors"]
        super().__init__(
            master=master,
            text=text,
            foreground=self.colors["text"],
            font=styling["font"],
            name=text.lower(),
        )
        self.button_group = button_group
        self.key = key
        self.text = text
        self.tab_nav_int = tab_nav_int
        self.tab_nav_str = tab_nav_str

        if tab_nav_str.get() == text:
            self.select_handler()

        self.pack(
            side=styling["side"],
            padx=styling["padx"],
            pady=styling["pady"],
            anchor=styling["anchor"],
        )
        self.bind("<Button-1>", self.select_handler)

        if context_menu:
            self.context_menu = context_menu
            self.bind("<Button-3>", self.open_context_menu)

    def open_context_menu(self, event) -> None:
        self.select_handler()
        self.context_menu.open_popup(event)

    def select_handler(self, *_args: int) -> None:
        """Callback method for when the label is clicked on."""
        if self.tab_nav_int is not None:
            self.tab_nav_int.set(self.key)
        self.tab_nav_str.set(self.text)
        for button in self.button_group:
            button.unselect()
        self.configure(foreground=self.colors["highlight"])

    def unselect(self) -> None:
        """Resets the text color."""
        self.configure(foreground=self.colors["text"])


class ContextMenu(tb.Frame):
    def __init__(self, app) -> None:
        super().__init__(master=app)
        self.app = app
        self.buttons = []
        self.app.bind("<Button-1>", self.destroy, add=True)

    def add_command(self, label, command) -> None:
        lbl = tb.Label(self, text=label)
        lbl.pack(fill="x", anchor="w", padx=5, pady=5)
        lbl.bind("<Button-1>", command)
        lbl.bind("<Enter>", self.hover_in)
        lbl.bind("<Leave>", self.hover_out)
        self.buttons.append(lbl)

    def open_popup(self, *_args) -> None:
        curr_x = self.app.winfo_pointerx() - self.app.winfo_x()
        curr_y = self.app.winfo_pointery() - self.app.winfo_y()
        self.place(x=curr_x + 1, y=curr_y + 1)
        self.lift()

    def hover_in(self, event) -> None:
        event.widget.configure(foreground="gray")

    def hover_out(self, event) -> None:
        event.widget.configure(foreground="white")

    def destroy(self, event=None) -> None:
        if event is not None:
            self.place_forget()
