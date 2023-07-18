import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs.dialogs import Messagebox

from config.definitions import *
from ..components.notifications import Notifications
from src.components.navigation import ButtonPanel, ContextMenu


class AutoLayoutFrame(tb.Frame):
    """Provides a frame class which supports automatic grid
    configuration and placement of labels.
    """

    def __init__(self, master, config, labels):
        super().__init__(master=master)
        for idx, weight in config["rowconfigure"].items():
            self.grid_rowconfigure(idx, weight=weight)
        for idx, weight in config["columnconfigure"].items():
            self.grid_columnconfigure(idx, weight=weight)

        for label in labels:
            tb.Label(self, text=label["text"], font=label["font"]).grid(
                row=label["row"],
                column=label["col"],
                rowspan=label["rowspan"],
                columnspan=label["columnspan"],
                padx=label["padx"],
                pady=label["pady"],
                sticky=label["sticky"],
            )


class RefreshMixin:
    """A mixin that allows a class to register its sub-components
    and to refresh those upon request.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registered_components = []

    def register(self, component):
        """Registers a component to be refreshed, whenever the refresh
        method of the tab frame is called.
        """
        self.registered_components.append(component)

    def refresh(self):
        """Refreshes all registered components inside this frame.

        This method is invoked by whichever parent holds those tab
        frames.
        """
        for component in self.registered_components:
            component.refresh()


class ListFrame(tb.Frame, RefreshMixin):
    """A frame with a default left sidebar to depict a selection of
    objects. The central frame will be filled with the given detail
    view frame and the given form frame.

    Parameters
    ----------
    form_edit : forms.Form
        A form for adding or editing an object of the list.
    detail_view : cards.DetailView
        A frame for displaying the selected item in great detail.
    """

    def __init__(
        self,
        master,
        app,
        db_service,
        db_session,
        form_edit,
        detail_view,
        db_delete_item,
    ):
        super().__init__(master=master)
        self.app = app
        self.db_service = db_service
        self.db_session = db_session
        self.form_edit = form_edit
        self.detail_view = detail_view
        self.db_delete_item = db_delete_item

        self.scrolled_frame = None
        self.item_detail_view = None

        self.objects = None
        self.item_key_var = tb.IntVar()
        self.item_str_var = tb.StringVar()
        self.item_str_var.trace("w", self.select_handler)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=7)
        self.grid_rowconfigure(0, weight=1)

        self.build_gui_components()

    def build_gui_components(self):
        """Create the GUI elements for this component."""
        for separator in TAB_FRAME_LIST["separators"]:
            sep_new = tb.Separator(self, orient=separator["orient"])
            sep_new.grid(
                row=separator["row"],
                column=separator["col"],
                rowspan=separator["rowspan"],
                sticky=separator["sticky"],
            )

        btn_new_item = tb.Button(
            self, text="New", bootstyle="success", command=self.open_form
        )
        btn_new_item.grid(row=2, column=0, pady=25)

        self.register(self)
        self.refresh()

    def select_handler(self, *_args):
        if self.item_detail_view:
            self.item_detail_view.grid_forget()
        item = self.objects[self.item_key_var.get()]
        self.item_detail_view = self.detail_view(self, self.app, item)
        self.item_detail_view.grid(row=0, rowspan=3, column=2, sticky="nsew")

    def refresh(self):
        if self.scrolled_frame:
            self.scrolled_frame.grid_remove()

        list_layout = TAB_FRAME_LIST["sidebar"]
        self.scrolled_frame = ScrolledFrame(master=self, autohide=True)
        self.scrolled_frame.grid(
            row=list_layout["row"],
            column=list_layout["col"],
            sticky=list_layout["sticky"],
        )

        # Context menu
        context_menu = ContextMenu(self.app)
        context_menu.add_command(label="Delete", command=self.delete_entry)

        # Item list
        items = self.db_service.get_all(self.db_session).all()
        item_dict = {}
        self.objects = {}
        for item in items:
            item_dict[item.id] = item.name
            self.objects[item.id] = item
        frm_item_list = ButtonPanel(
            parent=self.scrolled_frame,
            ttk_string_var=self.item_str_var,
            labels=item_dict,
            styling=LIST_ITEM,
            ttk_key_var=self.item_key_var,
            context_menu=context_menu,
        )
        frm_item_list.pack(expand=True, fill="both")

    def open_form(self):
        """Create a new form instance and put it on the grid layout."""
        form = self.form_edit(self, self.app, self.db_service, self.db_session)
        form.grid(row=0, rowspan=3, column=2, sticky="nsew")

    def delete_entry(self, *_args):
        usr_answ = Messagebox.okcancel(
            message="Are you sure you want to delete that entry?",
            title="Attention!",
        )
        if usr_answ == "OK":
            status = self.db_service.delete(
                self.db_session, self.item_key_var.get()
            )
            self.refresh()
            if status == 1:
                Notifications.show_info(
                    message="The entry has been deleted from the database."
                )
            elif status == 0:
                Notifications.show_error(
                    message="The entry couldn't be deleted."
                )
            else:
                Notifications.show_error(
                    message="There has been an unknown error!"
                )
