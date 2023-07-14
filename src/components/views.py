import ttkbootstrap as tb

from config.definitions import *
from .. components.frames import AutoLayoutFrame
from .. components.forms import CustomScrolledText


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
    def __init__(self, master, project):
        super().__init__(
            master=master,
            layout=VIEW_PROJECT_DETAIL
        )
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
