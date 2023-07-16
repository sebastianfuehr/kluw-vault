import ttkbootstrap as tb
from ttkbootstrap.dialogs.dialogs import Messagebox

from config.definitions import *
from .. components.notifications import Notifications
from .. components.frames import AutoLayoutFrame
from .. components.navigation import ButtonPanel, ContextMenu
from .. components.forms import ProjectForm
from ..controller.activity_service import ActivityService
from .. controller.project_service import ProjectService


class DetailView(AutoLayoutFrame):
    """A generic class to depict objects in great detail.

    Parameters
    ----------
    layout : dict
        A dictionary defining the layout of the component. Has to
        contain the variables specified below:
        - rowconfigure : dict(row_idx, weight)
        - columnconfigure : dict(col_idx, weight)
        - labels : dict
    """
    def __init__(self, master, layout):
        super().__init__(
            master=master,
            config=layout['grid-config'],
            labels=layout['labels']
        )

        btn = VIEW_BTN_EDIT
        btn_edit = tb.Button(
            self,
            text=btn['text'])
        btn_edit.bind('<Button-1>', self.open_edit_form)
        btn_edit.place(
            relx=btn['relx'],
            rely=btn['rely'],
            anchor=btn['anchor']
        )

    def open_edit_form(self, *_args):
        """Open a form for editing the selected entity.
        """
        print('Open edit form')


class ProjectDetailView(DetailView):
    def __init__(self, master, app, project):
        super().__init__(
            master=master,
            layout=VIEW_PROJECT_DETAIL
        )
        self.app = app
        self.project = project

        self.build_gui_components()

    def build_gui_components(self):
        CustomLabel(
            self,
            text=self.project.name,
            layout=VIEW_PROJECT_DETAIL['lbl_name']
        )

        # Category
        category_name = '-'
        if self.project.project_category is not None:
            category_name = self.project.project_category.name
        CustomLabel(
            self,
            text=category_name,
            layout=VIEW_PROJECT_DETAIL['lbl_category']
        )

        # Description
        description = self.project.description
        print(description)
        if description is None:
            description = '-'
        CustomLabel(
            self,
            text=description,
            layout=VIEW_PROJECT_DETAIL['lbl_description'],
            wraplength=600
        )

        # Activities
        CustomEntityItemList(
            master=self,
            app=self.app,
            entity=self.project,
            db_get_by_id=ActivityService.get_by_project_id,
            db_merge=None,
            db_delete=ActivityService.delete,
            db_session=self.app.session,
            form_edit=None,
            layout=VIEW_PROJECT_DETAIL['lst_activities']
        )

    def refresh(self, project):
        self.project = project
        print('Refresh ProjectDetailView')

#######################################################################
# CUSTOM DETAILVIEW WIDGETS
#######################################################################
class CustomLabel(tb.Label):
    def __init__(self, master, text, layout, **kwargs):
        super().__init__(
            master=master,
            text=text,
            font=layout['font'],
            **kwargs
        )
        self.grid(
            row=layout['row'],
            column=layout['col'],
            rowspan=layout['rowspan'],
            columnspan=layout['columnspan'],
            sticky=layout['sticky'],
            padx=layout['padx'],
            pady=layout['pady']
        )


class CustomEntityItemList(tb.Frame):
    """An interactive list of items, belonging to a specific entity.

    Supports an automatic implementation of a context menu.
    """
    def __init__(
            self,
            master,
            app,
            entity,
            db_get_by_id,
            db_merge,
            db_delete,
            db_session,
            form_edit,
            layout,
            **kwargs
        ):
        super().__init__(master=master, **kwargs)
        self.grid(
            row=layout['row'],
            column=layout['col'],
            rowspan=layout['rowspan'],
            columnspan=layout['columnspan'],
            sticky=layout['sticky'],
            padx=layout['padx'],
            pady=layout['pady']
        )
        self.app = app
        self.entity = entity
        self.db_get_by_id = db_get_by_id
        self.db_merge = db_merge
        self.db_delete = db_delete
        self.db_session = db_session
        self.form_edit = form_edit

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.item_key_var = tb.IntVar()
        self.item_name_var = tb.StringVar()

        self.item_list = None

        btn_pady = (10,0 )
        tb.Button(
            self,
            text='+',
            width=2,
            command=self.add_item
        ).grid(row=1, column=1, sticky='e', padx=10, pady=btn_pady)
        tb.Button(
            self,
            text='E',
            width=2,
            command=self.edit_item
        ).grid(row=1, column=2, sticky='e', padx=10, pady=btn_pady)
        tb.Button(
            self,
            text='-',
            width=2,
            command=self.delete_item
        ).grid(row=1, column=3, sticky='e', padx=10, pady=btn_pady)

        self.refresh()

    def refresh(self):
        """Populate the list with items.
        """
        items = self.db_get_by_id(self.db_session, self.entity.id)
        item_dict = {}
        for item in items:
            item_dict[item.id] = item.name
        print(item_dict)

        context_menu = ContextMenu(self.app)
        context_menu.add_command(label='Edit', command=self.edit_item)
        context_menu.add_command(label='Delete', command=self.delete_item)

        self.item_list = ButtonPanel(
            parent=self,
            ttk_string_var=self.item_name_var,
            labels=item_dict,
            styling=LIST_ITEM,
            ttk_key_var=self.item_key_var,
            borderwidth=1,
            relief='solid',
            context_menu=context_menu
        )
        self.item_list.grid(row=0, column=0, columnspan=4, sticky='nsew')

    def add_item(self, *_args):
        print(f'Add item')

    def edit_item(self, *_args):
        print(f'Edit item {self.item_key_var.get()}: {self.item_name_var.get()}')

    def delete_item(self, *_args):
        print(f'Delete item {self.item_key_var.get()}: {self.item_name_var.get()}')
        usr_answ = Messagebox.okcancel(
            message='Are you sure you want to delete that entry?',
            title='Attention!'
        )
        if usr_answ == 'OK':
            self.db_delete(self.db_session, self.item_key_var.get())
