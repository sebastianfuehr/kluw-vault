import ttkbootstrap as tb

from config.definitions import *
from .. components.frames import AutoLayoutFrame
from .. components.navigation import ButtonPanel
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
            entity=self.project,
            db_service_method=ActivityService.get_by_project_id,
            db_session=self.app.session,
            form_edit=ProjectForm,
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
    """
    def __init__(
            self,
            master,
            entity,
            db_service_method,
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
        self.entity = entity
        self.db_service_method = db_service_method
        self.db_session = db_session
        self.form_edit = form_edit

        self.columnconfigure(0, weight=1)

        self.item_key_var = tb.IntVar()
        self.item_name_var = tb.StringVar()

        self.item_list = None

        tb.Button(
            self,
            text='+',
            width=2
        ).grid(row=1, column=1, sticky='e', padx=10)
        tb.Button(
            self,
            text='-',
            width=2
        ).grid(row=1, column=2, sticky='e', padx=10)

        self.refresh()

    def refresh(self):
        """Populate the list with items.
        """
        items = self.db_service_method(self.db_session, self.entity.id)
        item_dict = {}
        for item in items:
            item_dict[item.id] = item.name
        print(item_dict)
        self.item_list = ButtonPanel(
            parent=self,
            ttk_string_var=self.item_name_var,
            labels=item_dict,
            styling=LIST_ITEM,
            ttk_key_var=self.item_key_var,
            borderwidth=1,
            relief='solid'
        )
        self.item_list.grid(row=0, column=0, columnspan=3, sticky='nsew')
