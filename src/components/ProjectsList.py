import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledText, ScrolledFrame

from config.definitions import *
from .. controller.project_service import ProjectService
from .. controller.activity_service import ActivityService


class ProjectsList(tb.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        frm_list_selection = tb.Frame(self)
        frm_list_selection.grid(row=0, column=0, sticky='ns')

        self.projects = ProjectService.get_all(self.app.session).all()
        self.selected_project_id = tb.IntVar(self, self.projects[0].id)
        self.buttons = [ProjectListItem(
            frm_list_selection,
            self.app,
            project,
            self.selected_project_id
        ) for project in self.projects]
        self.selected_project_id.trace('w', self.__update_screen)

        sep_new_project = tb.Separator(self)
        sep_new_project.grid(row=1, column=0, sticky='ew')

        btn_new_project = tb.Button(self, text='New', bootstyle='success', command=self.new_project_frame)
        btn_new_project.grid(row=2, column=0, pady=25)

        sep_list_seleection = tb.Separator(self, orient='vertical')
        sep_list_seleection.grid(row=0, column=1, rowspan=3, sticky='ns')

        self.project_detail_panel = ProjectDetailPanel(self, self.app, self.projects[0])
        self.project_detail_panel.grid(row=0, rowspan=3, column=2, sticky='nsew')

    def __update_screen(self, *args):
        [button.unselect() for button in self.buttons]
        new_project = next(filter(lambda el: el.id == self.selected_project_id.get(), self.projects), None)
        self.project_detail_panel.display_project(new_project)

    def new_project_frame(self):
        self.new_project_frame = NewProjectForm(self)
        self.new_project_frame.grid(row=0, rowspan=3, column=0, columnspan=3, sticky='nsew')


class ProjectListItem(tb.Label):
    def __init__(self, parent, app, project, selected_project_id):
        super().__init__(master=parent, text=project.name)
        self.app = app
        self.project = project
        self.selected_project_id = selected_project_id
        self.bind('<Button-1>', self.__select_handler)

        self.pack(side='top', padx=10, pady=(10, 0), fill='x')

        if selected_project_id.get() == project.id:
            self.__select_handler()

    def __select_handler(self, *args):
        self.selected_project_id.set(self.project.id)
        self.configure(foreground=HIGHLIGHT_COLOR)

    def unselect(self):
        self.configure(foreground=TEXT_COLOR)


class ProjectDetailPanel(tb.Frame):
    def __init__(self, parent, app, project):
        super().__init__(master=parent)
        self.edit_mode = False
        self.project = project
        self.project_name = tb.StringVar(self, self.project.name)
        self.project_category = tb.StringVar(self, self.project.project_category.name)

        self.grid_columnconfigure((1), weight=1)

        lbl_padx = 10
        lbl_pady = (15, 5)
        inp_pady = 5

        lbl_heading = tb.Label(
            self,
            textvariable=self.project_name,
            font=(None, 36, 'bold')
        )
        lbl_heading.grid(row=0, column=0, columnspan=2, padx=lbl_padx, pady=25, sticky='ew')

        self.btn_edit_save = tb.Button(
            self,
            text='Edit',
            command=self.__select_handler,
            bootstyle='info'
        )
        self.btn_edit_save.place(relx=0.98, rely=0.02, anchor='ne')

        lbl_category_heading = tb.Label(
            self,
            text='Category:'
        )
        lbl_category_heading.grid(row=1, column=1, padx=lbl_padx, pady=lbl_pady, sticky='w')
        inp_category_value = tb.Combobox(self,
                                         textvariable=self.project_category,
                                         font=COMBO_BOX_FONT,
                                         state='disabled')
        inp_category_value.grid(row=2, column=1, padx=lbl_padx, pady=inp_pady, sticky='nsew')

        lbl_description_heading = tb.Label(
            self,
            text='Description:'
        )
        lbl_description_heading.grid(row=3, column=1, padx=lbl_padx, pady=lbl_pady, sticky='w')
        self.inp_description_value = ScrolledText(
            self,
            text=self.project.description,
            height=4,
            state='disabled'
        )
        self.inp_description_value.grid(row=4, column=1, padx=lbl_padx, pady=inp_pady, sticky='nsew')

        lbl_activities_heading = tb.Label(
            self,
            text='Activities:'
        )
        lbl_activities_heading.grid(row=5, column=1, padx=lbl_padx, pady=lbl_pady, sticky='w')
        self.activities_list = ActivitiesList(self, self.project)
        self.activities_list.grid(row=6, column=1, padx=lbl_padx, pady=inp_pady, sticky='nsew')

    def display_project(self, project):
        print(f'{project.id}: {project.name}')
        self.project = project
        self.project_name.set(project.name)
        self.project_category.set(project.project_category.name)

        self.inp_description_value.text.delete(1.0, tb.END)
        if project.description is not None:
            self.inp_description_value.text.insert(1.0, project.description)
        self.activities_list.build_list(project)

    def __select_handler(self, *args):
        if self.edit_mode:
            self.btn_edit_save.configure(text='Edit')
            self.edit_mode = False
        else:
            self.btn_edit_save.configure(text='Save')
            self.edit_mode = True


class ActivitiesList(tb.Frame):
    def __init__(self, parent, project):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.build_list(project)

    def build_list(self, project):
        self.frm_activities = ScrolledFrame(
            self,
            height=120,
            scrollheight=120,
            borderwidth=1,
            relief='solid'
        )
        self.frm_activities.grid(row=0, column=0, sticky='nsew')

        for activity in project.activities:
            lbl_activity = tb.Label(
                self.frm_activities,
                text=activity.name
            )
            lbl_activity.pack(fill='x', anchor='w')


class NewProjectForm(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 9), weight=1)

        self.category_id_var = tb.StringVar()

        inp_lbl_font = (None, 14, 'bold')
        inp_lbl_pady = 10
        inp_font = (None, 14)
        inp_pady = (0, 10)

        lbl_heading = tb.Label(
            self, text='Create New Project', font=FORM_HEADING_FONT
        )
        lbl_heading.grid(row=1, pady=(0, 30))

        lbl_name = tb.Label(self, text='Name', font=inp_lbl_font)
        lbl_name.grid(row=2, pady=inp_lbl_pady)
        inp_name = tb.Entry(self, font=inp_font)
        inp_name.grid(row=3, pady=inp_pady)

        lbl_description = tb.Label(self, text='Description', font=inp_lbl_font)
        lbl_description.grid(row=4, pady=inp_lbl_pady)
        inp_description = tb.Entry(self, font=inp_font)
        inp_description.grid(row=5, pady=inp_pady)

        lbl_project_category = tb.Label(
            self, text='Project Category', font=inp_lbl_font
        )
        lbl_project_category.grid(row=6, pady=inp_lbl_pady)
        inp_project_category = tb.Combobox(self,
                                           textvariable=self.category_id_var,
                                           font=inp_font)
        inp_project_category.grid(row=7, pady=inp_pady)

        btn_save = tb.Button(self, text='Save', bootstyle='success')
        btn_save.grid(row=8, pady=(30, 0))

        btn_close_form = tb.Label(self, text='X', font=(None, 24))
        btn_close_form.bind('<Button-1>', self.close_form)
        btn_close_form.place(relx=0.98, rely=0.02, anchor='ne')

    def close_form(self, *args):
        self.grid_forget()
