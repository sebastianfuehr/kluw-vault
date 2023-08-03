import pandas as pd
import ttkbootstrap as tb
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.scrolled import ScrolledFrame

from ..components.forms import ActivityForm, ProjectCategoryGoalForm, ProjectForm
from ..components.frames import AutoLayoutFrame
from ..components.navigation import ButtonPanel, ContextMenu
from ..components.notifications import Notifications
from ..components.visuals import GraphTimePerDay
from ..controller.activity_service import ActivityService
from ..controller.project_category_goal_service import ProjectCategoryGoalService
from ..controller.project_service import ProjectService


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

    def __init__(self, master, app, layout):
        super().__init__(
            master=master,
            config=layout["grid-config"],
            labels=layout["labels"],
        )

        btn = app.definitions.VIEW_BTN_EDIT
        btn_edit = tb.Button(self, text=btn["text"])
        btn_edit.bind("<Button-1>", self.open_edit_form)
        btn_edit.place(relx=btn["relx"], rely=btn["rely"], anchor=btn["anchor"])

    def open_edit_form(self, *_args):
        """Open a form for editing the selected entity."""
        print("Open edit form")


class ProjectDetailView(DetailView):
    def __init__(self, master, app, project):
        super().__init__(
            master=master, app=app, layout=app.definitions.VIEW_PROJECT_DETAIL
        )
        self.app = app
        self.project = project

        self.activity_id_var = tb.IntVar()
        self.activity_name_var = tb.StringVar()

        self.build_gui_components()

    def build_gui_components(self):
        CustomLabel(
            self,
            text=self.project.name,
            layout=self.app.definitions.VIEW_PROJECT_DETAIL["lbl_name"],
        )

        # Category
        category_name = "-"
        if self.project.project_category is not None:
            category_name = self.project.project_category.name
        CustomLabel(
            self,
            text=category_name,
            layout=self.app.definitions.VIEW_PROJECT_DETAIL["lbl_category"],
        )

        # Description
        description = self.project.description
        if description is None:
            description = "-"
        CustomLabel(
            self,
            text=description,
            layout=self.app.definitions.VIEW_PROJECT_DETAIL["lbl_description"],
            wraplength=600,
        )
        self.refresh()

    def refresh(self):
        # Activities
        items = ActivityService.get_by_project_id(self.app.session, self.project.id)
        item_dict = {}
        for item in items:
            item_dict[item.id] = item.name

        CustomEntityItemList(
            master=self,
            app=self.app,
            entity=self.project,
            item_key_var=self.activity_id_var,
            item_name_var=self.activity_name_var,
            item_dict=item_dict,
            cmd_add_item=self.open_activity_creation_form,
            cmd_edit_item=self.open_activity_edit_form,
            cmd_delete_item=self.delete_activity,
            layout=self.app.definitions.VIEW_PROJECT_DETAIL["lst_activities"],
        )

        # Time per day
        time_entries = self.app.dc.time_entry_df
        time_entries = time_entries[time_entries["Project Name"] == self.project.name]

        # Group data
        duration_per_day = time_entries.groupby(pd.Grouper(key="Date", freq="D"))[
            "Duration"
        ].sum()
        duration_per_day = duration_per_day.reset_index()
        duration_per_day["Hours"] = (
            duration_per_day["Duration"].dt.total_seconds() / 60 / 60
        )
        graph_layout = self.app.definitions.VIEW_PROJECT_DETAIL["graph_time_per_day"]
        GraphTimePerDay(
            self, self.app, duration_per_day, value_column_name="Hours"
        ).grid(
            row=graph_layout["row"],
            column=graph_layout["col"],
            rowspan=graph_layout["rowspan"],
            columnspan=graph_layout["columnspan"],
            sticky=graph_layout["sticky"],
            padx=graph_layout["padx"],
            pady=graph_layout["pady"],
        )

    def open_activity_creation_form(self, *_args):
        frm_dict = self.app.definitions.VIEW_PROJECT_DETAIL["frm_edit_activity"]
        form = ActivityForm(
            master=self,
            app=self.app,
            db_service=ActivityService,
            db_session=self.app.session,
            project_id=self.project.id,
        )
        form.grid(
            row=frm_dict["row"],
            column=frm_dict["col"],
            rowspan=frm_dict["rowspan"],
            columnspan=frm_dict["columnspan"],
            sticky=frm_dict["sticky"],
            padx=frm_dict["padx"],
            pady=frm_dict["pady"],
        )

    def open_activity_edit_form(self, *_args):
        frm_dict = self.app.definitions.VIEW_PROJECT_DETAIL["frm_edit_activity"]
        activity = ActivityService.get_by_id(
            self.app.session, self.activity_id_var.get()
        )

        form = ActivityForm(
            master=self,
            app=self.app,
            db_service=ActivityService,
            db_session=self.app.session,
            project_id=self.project.id,
            activity=activity,
        )
        form.grid(
            row=frm_dict["row"],
            column=frm_dict["col"],
            rowspan=frm_dict["rowspan"],
            columnspan=frm_dict["columnspan"],
            sticky=frm_dict["sticky"],
            padx=frm_dict["padx"],
            pady=frm_dict["pady"],
        )

    def delete_activity(self, *_args):
        msg = f'Are you sure you want to delete the activity "{self.activity_name_var.get()}" in the "{self.project.name}" project?'
        usr_answ = Messagebox.okcancel(message=msg, title="Attention!")
        if usr_answ == "OK":
            ActivityService.delete(self.app.session, self.activity_id_var.get())
        self.refresh()


class CategoryDetailView(DetailView):
    def __init__(self, master, app, project_category):
        super().__init__(
            master=master, app=app, layout=app.definitions.VIEW_PROJECT_CATEGORY_DETAIL
        )
        self.app = app
        self.project_category = project_category

        self.project_id_var = tb.IntVar()
        self.project_name_var = tb.StringVar()
        self.category_goal_id_var = tb.IntVar()

        self.build_gui_components()

    def build_gui_components(self):
        CustomLabel(
            self,
            text=self.project_category.name,
            layout=self.app.definitions.VIEW_PROJECT_CATEGORY_DETAIL["lbl_name"],
        )

        # Description
        description = self.project_category.description
        if description is None:
            description = "-"
        CustomLabel(
            self,
            text=description,
            layout=self.app.definitions.VIEW_PROJECT_CATEGORY_DETAIL["lbl_description"],
            wraplength=600,
        )
        self.refresh()

    def refresh(self):
        # Projects
        items = ProjectService.get_by_category_id(
            self.app.session, self.project_category.id
        )
        item_dict = {}
        for item in items:
            item_dict[item.id] = item.name

        CustomEntityItemList(
            master=self,
            app=self.app,
            entity=self.project_category,
            item_key_var=self.project_id_var,
            item_name_var=self.project_name_var,
            item_dict=item_dict,
            cmd_add_item=None,
            cmd_edit_item=None,
            cmd_delete_item=None,
            layout=self.app.definitions.VIEW_PROJECT_CATEGORY_DETAIL["lst_projects"],
        )

        goals = ProjectCategoryGoalService.get_by_category_id(
            self.app.session, self.project_category.id
        )
        goal_dict = {}
        for goal in goals:
            goal_dict[goal.id] = goal
        ProjectCategoryGoalList(
            master=self,
            app=self.app,
            item_key_var=self.category_goal_id_var,
            item_dict=goal_dict,
            cmd_edit_item=self.open_goal_edit_form,
            layout=self.app.definitions.VIEW_PROJECT_CATEGORY_DETAIL["lst_goals"],
        )

    def open_goal_edit_form(self, *_args):
        frm_dict = self.app.definitions.VIEW_PROJECT_CATEGORY_DETAIL[
            "frm_edit_activity"
        ]
        goal = None
        try:
            goal = ProjectCategoryGoalService.get_by_id(
                self.app.session, self.category_goal_id_var.get()
            )
        except TypeError:
            pass
        form = ProjectCategoryGoalForm(
            master=self,
            app=self.app,
            db_service=ProjectCategoryGoalService,
            db_session=self.app.session,
            category_id=self.project_category.id,
            goal=goal,
        )
        form.grid(
            row=frm_dict["row"],
            column=frm_dict["col"],
            rowspan=frm_dict["rowspan"],
            columnspan=frm_dict["columnspan"],
            sticky=frm_dict["sticky"],
            padx=frm_dict["padx"],
            pady=frm_dict["pady"],
        )

    def open_activity_creation_form(self, *_args):
        frm_dict = self.app.definitions.VIEW_PROJECT_DETAIL["frm_edit_activity"]
        form = ActivityForm(
            master=self,
            app=self.app,
            db_service=ActivityService,
            db_session=self.app.session,
            project_id=self.project_category.id,
        )
        form.grid(
            row=frm_dict["row"],
            column=frm_dict["col"],
            rowspan=frm_dict["rowspan"],
            columnspan=frm_dict["columnspan"],
            sticky=frm_dict["sticky"],
            padx=frm_dict["padx"],
            pady=frm_dict["pady"],
        )

    def open_activity_edit_form(self, *_args):
        frm_dict = self.app.definitions.VIEW_PROJECT_DETAIL["frm_edit_activity"]
        activity = ActivityService.get_by_id(
            self.app.session, self.project_id_var.get()
        )

        form = ActivityForm(
            master=self,
            app=self.app,
            db_service=ActivityService,
            db_session=self.app.session,
            project_id=self.project_category.id,
            activity=activity,
        )
        form.grid(
            row=frm_dict["row"],
            column=frm_dict["col"],
            rowspan=frm_dict["rowspan"],
            columnspan=frm_dict["columnspan"],
            sticky=frm_dict["sticky"],
            padx=frm_dict["padx"],
            pady=frm_dict["pady"],
        )

    def delete_activity(self, *_args):
        msg = f'Are you sure you want to delete the activity "{self.project_name_var.get()}" in the "{self.project_category.name}" project?'
        usr_answ = Messagebox.okcancel(message=msg, title="Attention!")
        if usr_answ == "OK":
            ActivityService.delete(self.app.session, self.project_id_var.get())
        self.refresh()


#######################################################################
# CUSTOM DETAILVIEW WIDGETS
#######################################################################
class CustomLabel(tb.Label):
    def __init__(self, master, text, layout, **kwargs):
        super().__init__(master=master, text=text, font=layout["font"], **kwargs)
        self.grid(
            row=layout["row"],
            column=layout["col"],
            rowspan=layout["rowspan"],
            columnspan=layout["columnspan"],
            sticky=layout["sticky"],
            padx=layout["padx"],
            pady=layout["pady"],
        )


class CustomEntityItemList(tb.Frame):
    """An interactive list of items, belonging to a specific entity.

    Supports an automatic implementation of a context menu.

    Parameters
    ----------
    layout : dict
        Information for how to place the list component itself and all
        it's subcomponents.
    form_layout : dict
        Information for how to place the the form for new and existing
        entities with regards to the **master** component.
    """

    def __init__(
        self,
        master,
        app,
        entity,
        item_key_var,
        item_name_var,
        item_dict,
        cmd_add_item,
        cmd_edit_item,
        cmd_delete_item,
        layout,
        **kwargs,
    ):
        super().__init__(master=master, **kwargs)
        self.grid(
            row=layout["row"],
            column=layout["col"],
            rowspan=layout["rowspan"],
            columnspan=layout["columnspan"],
            sticky=layout["sticky"],
            padx=layout["padx"],
            pady=layout["pady"],
        )
        self.app = app
        self.entity = entity
        self.item_key_var = item_key_var
        self.item_name_var = item_name_var
        self.cmd_edit_item = cmd_edit_item
        self.cmd_delete_item = cmd_delete_item

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.scrolled_frame = None
        self.item_list = None

        for separator in self.app.definitions.CUSTOM_ENTITIY_ITEM_LIST["separators"]:
            sep_new = tb.Separator(self, orient=separator["orient"])
            sep_new.grid(
                row=separator["row"],
                column=separator["col"],
                rowspan=separator["rowspan"],
                sticky=separator["sticky"],
            )

        btn_pady = (10, 0)
        btn_add = tb.Button(self, text="+", width=2, command=cmd_add_item)
        btn_add.grid(row=3, column=0, sticky="e", padx=10, pady=btn_pady)

        self.refresh(item_dict)

    def refresh(self, item_dict):
        """Populate the list with items."""
        if self.scrolled_frame:
            self.scrolled_frame.grid_remove()

        list_layout = self.app.definitions.VIEW_PROJECT_DETAIL["lst_activities"]
        self.scrolled_frame = ScrolledFrame(master=self, autohide=True, height=180)
        self.scrolled_frame.grid(row=1, column=0, sticky="nsew")

        context_menu = ContextMenu(self.app)
        context_menu.add_command(label="Edit", command=self.cmd_edit_item)
        context_menu.add_command(label="Delete", command=self.cmd_delete_item)

        self.item_list = ButtonPanel(
            parent=self.scrolled_frame,
            ttk_string_var=self.item_name_var,
            labels=item_dict,
            styling=self.app.definitions.LIST_ITEM,
            ttk_key_var=self.item_key_var,
            context_menu=context_menu,
        )
        self.item_list.pack(expand=True, fill="both")

    def add_item(self, *_args):
        """Create a new form instance and put it on the grid layout."""
        form = self.form_edit(
            self.master,
            self.app,
            self.db_service,
            self.db_session,
            project_id=self.item_key_var.get(),
        )
        form.grid(
            row=self.form_layout["row"],
            column=self.form_layout["col"],
            rowspan=self.form_layout["rowspan"],
            columnspan=self.form_layout["columnspan"],
            sticky=self.form_layout["sticky"],
            padx=self.form_layout["padx"],
            pady=self.form_layout["pady"],
        )


class ProjectCategoryGoalList(AutoLayoutFrame):
    def __init__(
        self, master, app, item_key_var, item_dict, cmd_edit_item, layout, **kwargs
    ):
        config = app.definitions.VIEW_PROJECT_CATEGORY_GOAL_DETAIL
        super().__init__(
            master=master,
            config=config["grid_config"],
            labels=config["labels"],
        )
        self.app = app
        self.item_key_var = item_key_var
        self.cmd_edit_item = cmd_edit_item

        self.grid(
            row=layout["row"],
            column=layout["col"],
            rowspan=layout["rowspan"],
            columnspan=layout["columnspan"],
            sticky=layout["sticky"],
            padx=layout["padx"],
            pady=layout["pady"],
        )

        for separator in config["separators"]:
            sep_new = tb.Separator(self, orient=separator["orient"])
            sep_new.grid(
                row=separator["row"],
                column=separator["col"],
                rowspan=separator["rowspan"],
                columnspan=separator["columnspan"],
                sticky=separator["sticky"],
            )

        btn_config = config["btn_edit"]
        row_config = config["row_min_label"]
        curr_row = row_config["row"]
        for goal_id, goal in item_dict.items():
            btn = tb.Button(
                self,
                text="Edit",
                width=btn_config["width"],
                command=lambda: self.open_edit_form(goal_id),
            ).grid(
                row=curr_row,
                column=btn_config["col"],
                sticky=btn_config["sticky"],
                padx=btn_config["padx"],
                pady=btn_config["pady"],
            )

            goal_values = goal.get_goal_list()
            goal_value_idx = 0
            for curr_col in range(row_config["col"], row_config["col"] + 7):
                lbl = tb.Label(
                    self,
                    text=goal_values[goal_value_idx],
                    width=row_config["width"],
                    font=row_config["font"],
                ).grid(
                    row=curr_row,
                    column=curr_col,
                    sticky=row_config["sticky"],
                    padx=row_config["padx"],
                    pady=row_config["pady"],
                )
                goal_value_idx += 1

        if len(item_dict.keys()) == 0:
            btn = tb.Button(
                self,
                text="New",
                width=btn_config["width"],
                command=lambda: self.cmd_edit_item(),
            ).grid(
                row=0,
                column=btn_config["col"],
                sticky=btn_config["sticky"],
                padx=btn_config["padx"],
                pady=btn_config["pady"],
            )

    def open_edit_form(self, item_id):
        self.item_key_var.set(item_id)
        self.cmd_edit_item()
