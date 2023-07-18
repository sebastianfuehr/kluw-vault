import ttkbootstrap as tb
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.scrolled import ScrolledText, ScrolledFrame
from ttkbootstrap.dialogs.dialogs import Messagebox
from datetime import datetime, timedelta

# Custom modules
from config.definitions import *
from ..components.frames import AutoLayoutFrame
from ..model.time_entry import TimeEntry
from ..model.project import Project
from ..model.project_category import ProjectCategory
from ..model.project_category_goal import ProjectCategoryGoal
from ..model.activity import Activity
from ..controller.time_entry_service import TimeEntryService
from ..controller.project_service import ProjectService
from ..controller.project_category_service import ProjectCategoryService
from ..controller.activity_service import ActivityService
from ..controller.project_category_goal_service import (
    ProjectCategoryGoalService,
)


class TimeEntryForm(tb.Frame):
    """A form for editing and adding new time entries."""

    def __init__(self, parent, app, new_entry_var):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.new_entry_var = new_entry_var

        self.entry_font = ("Helvetica", 16)

        self.build_form_components()
        self.set_time_entry(None)

    def build_form_components(self):
        """Creates the GUI widgets for this component."""
        frm_padx = 10
        lbl_pax = 10
        field_padx = 0
        inp_width = 14

        frame_heading = tb.Frame(self)
        frame_heading.pack(fill="x", padx=frm_padx, pady=10)

        lbl_heading = tb.Label(
            frame_heading, text="Time Entry", font=(None, 24, "bold")
        )
        lbl_heading.pack(side="left")

        self.btn_new_entry = tb.Button(
            frame_heading,
            text="New",
            bootstyle="success",
            command=self.__select_handler_new_entry,
        )
        self.btn_new_entry.pack(side="right")

        scr_frame = ScrolledFrame(self, padding=0, width=315)
        scr_frame.pack(expand=True, fill="both", padx=0)
        scr_frame.grid_columnconfigure(1, weight=1)

        lbl_te_date = tb.Label(scr_frame, text="Date:")
        lbl_te_date.grid(column=0, row=1, sticky="w", padx=lbl_pax, pady=5)
        self.te_date = tb.Entry(
            scr_frame, width=inp_width, font=self.entry_font, justify="center"
        )
        self.te_date.grid(column=1, row=1, sticky="e", padx=field_padx, pady=5)

        lbl_te_weekday = tb.Label(scr_frame, text="Day:")
        lbl_te_weekday.grid(column=0, row=2, sticky="w", padx=lbl_pax, pady=5)
        self.te_weekday = tb.Label(scr_frame, width=inp_width, anchor="center")
        self.te_weekday.grid(
            column=1, row=2, sticky="e", padx=field_padx, pady=5
        )
        self.te_weekday["text"] = datetime.today().strftime("%a")

        lbl_te_start = tb.Label(scr_frame, text="Start:")
        lbl_te_start.grid(column=0, row=3, sticky="w", padx=lbl_pax, pady=5)
        self.te_start = tb.Entry(
            scr_frame, font=self.entry_font, width=inp_width, justify="center"
        )
        self.te_start.grid(
            column=1, row=3, sticky="e", padx=field_padx, pady=5
        )

        lbl_te_end = tb.Label(scr_frame, text="End:")
        lbl_te_end.grid(column=0, row=4, sticky="w", padx=lbl_pax, pady=5)
        self.te_end = tb.Entry(
            scr_frame, font=self.entry_font, width=inp_width, justify="center"
        )
        self.te_end.grid(column=1, row=4, sticky="e", padx=field_padx, pady=5)

        lbl_te_pause = tb.Label(scr_frame, text="Pause:")
        lbl_te_pause.grid(column=0, row=5, sticky="w", padx=lbl_pax, pady=5)
        self.te_pause = tb.Entry(
            scr_frame, font=self.entry_font, width=inp_width, justify="center"
        )
        self.te_pause.grid(
            column=1, row=5, sticky="e", padx=field_padx, pady=5
        )

        lbl_te_duration = tb.Label(scr_frame, text="Duration:")
        lbl_te_duration.grid(column=0, row=6, sticky="w", padx=lbl_pax, pady=5)
        self.te_duration = tb.Label(
            scr_frame, width=inp_width, anchor="center"
        )
        self.te_duration.grid(
            column=1, row=6, sticky="e", padx=field_padx, pady=5
        )
        self.te_duration["text"] = "00:00:00"

        # Project combobox
        projects = ProjectService.get_all(self.app.session).all()
        project_names = [project.name for project in projects]
        if len(project_names) == 0:
            init_proj_name = None
        else:
            init_proj_name = project_names[0]
        self.selected_project = tb.StringVar(value=init_proj_name)
        self.selected_project.trace("w", self.__populate_activities_list)

        lbl_te_project = tb.Label(scr_frame, text="Project:")
        lbl_te_project.grid(column=0, row=7, sticky="w", padx=lbl_pax, pady=5)
        self.te_project = tb.Combobox(
            scr_frame,
            textvariable=self.selected_project,
            font=self.entry_font,
            width=12,
            justify="right",
        )
        self.te_project.grid(
            column=1, row=7, sticky="e", padx=field_padx, pady=5
        )
        self.te_project["values"] = project_names

        # Activity combobox
        self.selected_activity = tb.StringVar()
        lbl_te_activity = tb.Label(scr_frame, text="Activity:")
        lbl_te_activity.grid(column=0, row=8, sticky="w", padx=lbl_pax, pady=5)
        self.te_activity = tb.Combobox(
            scr_frame,
            textvariable=self.selected_activity,
            font=self.entry_font,
            width=12,
            justify="right",
        )
        self.te_activity.grid(
            column=1, row=8, sticky="e", padx=field_padx, pady=5
        )
        self.__populate_activities_list()

        self.te_alone_var = tb.IntVar(value=1)
        lbl_te_alone = tb.Label(scr_frame, text="Alone:")
        lbl_te_alone.grid(column=0, row=9, sticky="w", padx=lbl_pax, pady=5)
        self.te_alone = tb.Checkbutton(
            scr_frame, variable=self.te_alone_var, bootstyle="round-toggle"
        )
        self.te_alone.grid(column=1, row=9, padx=field_padx, pady=5)

        lbl_te_tags = tb.Label(scr_frame, text="Tags:")
        lbl_te_tags.grid(column=0, row=10, sticky="nw", padx=lbl_pax, pady=5)
        self.te_tags = ScrolledText(
            scr_frame,
            font=self.entry_font,
            width=inp_width,
            height=3,
            autohide=True,
        )
        self.te_tags.grid(
            column=1, row=10, sticky="e", padx=field_padx, pady=5
        )
        ToolTip(self.te_tags, text="One tag per line.")

        lbl_te_comment = tb.Label(scr_frame, text="Comment:")
        lbl_te_comment.grid(
            column=0, row=11, columnspan=2, sticky="w", padx=lbl_pax, pady=5
        )
        self.te_comment = ScrolledText(
            scr_frame,
            font=self.entry_font,
            width=inp_width,
            height=3,
            autohide=True,
        )
        self.te_comment.grid(
            column=0, row=12, columnspan=2, sticky="ew", padx=(10, 0), pady=5
        )

        # Button
        self.btn_save_entry = tb.Button(
            scr_frame, text="Save", command=self.save_entry, width=14
        )
        self.btn_save_entry.grid(
            column=0, row=13, columnspan=2, padx=10, pady=20
        )

    def __populate_activities_list(self, *args):
        self.selected_activity.set("")
        project_name = self.selected_project.get()
        if project_name == "":
            self.te_activity["values"] = []
        else:
            project = ProjectService.get_project_by_name(
                self.app.session, project_name
            )
            activity_names = [activity.name for activity in project.activities]
            self.te_activity["values"] = activity_names
            if len(activity_names) > 0:
                self.selected_activity.set(activity_names[0])

    def __select_handler_new_entry(self, *args):
        if self.new_entry_var.get():
            self.new_entry_var.set(False)
        else:
            self.new_entry_var.set(True)
        self.form_for_new_entry()

    def form_for_new_entry(self):
        """Callback wrapper for set_tim_entry(None)."""
        self.set_time_entry(None)
        if self.new_entry_var.get():
            self.btn_new_entry.configure(bootstyle="danger", text="Cancel")
        else:
            self.btn_new_entry.configure(bootstyle="success", text="New")

    def set_time_entry(self, time_entry: TimeEntry):
        self.time_entry = time_entry
        self.__populate_fields()

    def __populate_fields(self):
        if self.time_entry is None:
            # Rest all fields
            self.te_date.delete(0, tb.END)
            self.te_date.insert(0, datetime.now().date())

            self.te_weekday["text"] = datetime.now().strftime("%a")

            self.te_start.delete(0, tb.END)
            self.te_start.insert(0, datetime.now().strftime("%H:%M:%S"))

            self.te_end.delete(0, tb.END)
            self.te_end.insert(0, datetime.now().strftime("%H:%M:%S"))

            self.te_pause.delete(0, tb.END)
            self.te_pause.insert(0, "0:00:00")

            # TODO: Extra method for calculating the duration outside of the
            # time entry instance
            self.te_duration["text"] = "0:00:00"

            self.selected_project.set("")
            self.selected_activity.set("")

            self.te_alone_var.set(1)
            self.te_tags.text.delete("1.0", tb.END)
            self.te_comment.text.delete("1.0", tb.END)
        else:
            # Fill form fields with time entry values
            self.te_date.delete(0, tb.END)
            self.te_date.insert(0, self.time_entry.get_date())

            self.te_weekday["text"] = self.time_entry.get_weekday()

            self.te_start.delete(0, tb.END)
            self.te_start.insert(0, self.time_entry.get_start_time())

            self.te_end.delete(0, tb.END)
            new_end_time = self.time_entry.get_end_time()
            if new_end_time is not None:
                self.te_end.insert(0, new_end_time)

            self.te_pause.delete(0, tb.END)
            self.te_pause.insert(0, self.time_entry.get_pause_timedelta())

            self.te_duration["text"] = self.time_entry.get_duration_timedelta()

            self.selected_project.set(self.time_entry.get_project_name())
            self.selected_activity.set(self.time_entry.get_activity_name())

            self.te_alone_var.set(int(self.time_entry.alone == "True"))

            self.te_tags.text.delete(1.0, tb.END)
            self.te_tags.text.insert(1.0, self.time_entry.tags)

            self.te_comment.text.delete(1.0, tb.END)
            self.te_comment.text.insert(1.0, self.time_entry.comment)

    def save_entry(self):
        """Parses the form contents to create a new time entry and save
        it to the database.
        """
        if self.time_entry is None:
            new_entry = TimeEntry(None)
        else:
            new_entry = self.time_entry

        date = self.te_date.get()
        new_entry.start = datetime.strptime(
            f"{date} {self.te_start.get()}", "%Y-%m-%d %H:%M:%S"
        )
        new_entry.stop = datetime.strptime(
            f"{date} {self.te_end.get()}", "%Y-%m-%d %H:%M:%S"
        )
        pause_datetime = datetime.strptime(self.te_pause.get(), "%H:%M:%S")
        pause_duration = timedelta(
            hours=pause_datetime.hour,
            minutes=pause_datetime.minute,
            seconds=pause_datetime.second,
        )
        new_entry.pause = int(pause_duration.total_seconds())
        proj_name = self.selected_project.get()
        new_entry.project_id = ProjectService.get_project_by_name(
            self.app.session, proj_name
        ).id
        new_entry.project = Project(id=new_entry.project_id, name=proj_name)
        activity_name = self.selected_activity.get()
        new_entry.activity_id = ActivityService.get_activity_id(
            self.app.session, activity_name, new_entry.project_id
        ).id
        new_entry.activity = Activity(
            id=new_entry.activity_id, name=activity_name
        )

        alone_int = self.te_alone_var.get()
        if alone_int is not None:
            new_entry.alone = alone_int

        new_entry.tags = self.te_tags.text.get(1.0, tb.END)
        new_entry.comment = self.te_comment.get(1.0, tb.END)

        TimeEntryService.merge(self.app.session, new_entry)

        if self.time_entry is None:
            self.parent.add_entry(te=new_entry)
        else:
            self.parent.update_entry(te=new_entry)

        self.new_entry_var.set(False)
        self.form_for_new_entry()


class Form(AutoLayoutFrame):
    """A generic class for an entity form. Automatically generates
    simple text labels from a list of dictionaries, as well as a
    generic close button for the form.
    """

    def __init__(self, master, config, db_service, db_session):
        super().__init__(
            master=master,
            config=config["grid-config"],
            labels=config["labels"],
        )
        self.master = master
        self.db_service = db_service
        self.db_session = db_session

        btn = FORM_BTN_CLOSE
        btn_close_form = tb.Label(self, text=btn["text"], font=btn["font"])
        btn_close_form.bind("<Button-1>", self.close_form)
        btn_close_form.place(
            relx=btn["relx"], rely=btn["rely"], anchor=btn["anchor"]
        )

    def close_form(self, *_args):
        """Close the currently opened form."""
        self.grid_forget()

    def save_entry(self, new_object):
        """Read the values from the form fields, create a new Python
        object, and save it into the database.
        """
        self.db_service.merge(self.db_session, new_object)
        self.master.refresh()
        self.close_form()


class ProjectForm(Form):
    """A form to create or edit a project entity."""

    def __init__(self, master, app, db_service, db_session):
        super().__init__(
            master=master,
            config=FORM_PROJECT_EDIT,
            db_service=db_service,
            db_session=db_session,
        )
        self.app = app
        self.db_session = db_session

        self.name_var = tb.StringVar()
        self.category_id_var = tb.IntVar()
        self.category_name_var = tb.StringVar()

        self.build_form_components()

    def build_form_components(self):
        """Create the GUI elements for this component."""
        # Name and description
        CustomEntry(
            master=self,
            tk_variable=self.name_var,
            layout=FORM_PROJECT_EDIT["inp_name"],
        )
        self.inp_description = CustomScrolledText(
            master=self, layout=FORM_PROJECT_EDIT["inp_description"]
        )

        # Project categories
        categories = {}
        for category in ProjectCategoryService.get_all(self.db_session).all():
            categories[category.id] = category.name
        self.inp_category = CustomCombobox(
            master=self,
            tk_key_var=self.category_id_var,
            tk_value_var=self.category_name_var,
            elements=categories,
            layout=FORM_PROJECT_EDIT["inp_category"],
        )

        # Submit form
        CustomButton(
            master=self,
            text="Save",
            command=self.save_entry,
            layout=FORM_PROJECT_EDIT["btn_save"],
        )

    def save_entry(self, *_args):
        """Read the values from the form fields, create a new Python
        object, and save it into the database.
        """
        if self.name_var.get() == "":
            Messagebox.show_error(
                message="You can't create a project without giving it a name!",
                title="Error",
                alert=self.app.settings["notifications.sound"].getboolean(
                    "error_messages"
                ),
            )
            return
        new_project = Project(id=None, name=self.name_var.get())

        # Project description
        description = self.inp_description.get_text()
        if description != "":
            new_project.description = description

        # Project category
        category_id = self.category_id_var.get()
        if category_id != 0:
            new_project.project_category = ProjectCategory(
                id=category_id, name=self.category_name_var.get()
            )
            new_project.project_category_id = category_id

        super().save_entry(new_project)


class ActivityForm(Form):
    """A form to create or edit a project activity entity."""

    def __init__(
        self, master, app, db_service, db_session, project_id, activity=None
    ):
        super().__init__(
            master=master,
            config=FORM_ACTIVITY_EDIT,
            db_service=db_service,
            db_session=db_session,
        )
        self.app = app
        self.db_session = db_session
        self.project_id = project_id
        self.activity = activity

        self.name_var = tb.StringVar()

        self.build_form_components()

    def build_form_components(self):
        """Create the GUI elements for this component."""
        # Build widgets
        CustomEntry(
            master=self,
            tk_variable=self.name_var,
            layout=FORM_ACTIVITY_EDIT["inp_name"],
        )
        self.inp_description = CustomScrolledText(
            master=self, layout=FORM_ACTIVITY_EDIT["inp_description"]
        )

        # Fill form
        if self.activity is not None:
            self.name_var.set(self.activity.name)
            self.inp_description.set_text(self.activity.description)

        # Submit form
        CustomButton(
            master=self,
            text="Save",
            command=self.save_entry,
            layout=FORM_ACTIVITY_EDIT["btn_save"],
        )

    def save_entry(self, *_args):
        """Read the values from the form fields, create a new Python
        object, and save it into the database.
        """
        if self.name_var.get() == "":
            Messagebox.show_error(
                message="You can't create an activity without giving it a name!",
                title="Error",
                alert=self.app.settings["notifications.sound"].getboolean(
                    "error_messages"
                ),
            )
            return
        new_activity = Activity(id=None, name=self.name_var.get())
        if self.activity is not None:
            new_activity.id = self.activity.id

        # Activity description
        description = self.inp_description.get_text()
        if description != "":
            new_activity.description = description

        # Project
        new_activity.project_id = self.project_id

        super().save_entry(new_activity)


class ProjectCategoryForm(Form):
    """A form to create or edit a project entity."""

    def __init__(self, master, app, db_service, db_session):
        super().__init__(
            master=master,
            config=FORM_PROJECT_CATEGORY_EDIT,
            db_service=db_service,
            db_session=db_session,
        )
        self.app = app
        self.db_session = db_session

        self.name_var = tb.StringVar()

        self.build_form_components()

    def build_form_components(self):
        """Create the GUI elements for this component."""
        # Name and description
        CustomEntry(
            master=self,
            tk_variable=self.name_var,
            layout=FORM_PROJECT_CATEGORY_EDIT["inp_name"],
        )
        self.inp_description = CustomScrolledText(
            master=self, layout=FORM_PROJECT_CATEGORY_EDIT["inp_description"]
        )

        # Submit form
        CustomButton(
            master=self,
            text="Save",
            command=self.save_entry,
            layout=FORM_PROJECT_CATEGORY_EDIT["btn_save"],
        )

    def save_entry(self, *_args):
        """Read the values from the form fields, create a new Python
        object, and save it into the database.
        """
        if self.name_var.get() == "":
            Messagebox.show_error(
                message="You can't create a project category without giving it a name!",
                title="Error",
                alert=self.app.settings["notifications.sound"].getboolean(
                    "error_messages"
                ),
            )
            return
        new_project_category = ProjectCategory(
            id=None, name=self.name_var.get()
        )

        # Project description
        description = self.inp_description.get_text()
        if description != "":
            new_project_category.description = description

        super().save_entry(new_project_category)


class ProjectCategoryGoalForm(Form):
    """A form to create or edit a project activity entity."""

    def __init__(
        self, master, app, db_service, db_session, category_id, goal=None
    ):
        super().__init__(
            master=master,
            config=FORM_PROJECT_CATEGORY_GOAL_EDIT,
            db_service=db_service,
            db_session=db_session,
        )
        self.app = app
        self.db_session = db_session
        self.category_id = category_id
        self.goal = goal

        self.min_monday_var = tb.IntVar()
        self.min_tuesday_var = tb.IntVar()
        self.min_wednesday_var = tb.IntVar()
        self.min_thursday_var = tb.IntVar()
        self.min_friday_var = tb.IntVar()
        self.min_saturday_var = tb.IntVar()
        self.min_sunday_var = tb.IntVar()

        self.build_form_components()

    def build_form_components(self):
        """Create the GUI elements for this component."""
        # Build widgets
        CustomEntry(
            master=self,
            tk_variable=self.min_monday_var,
            layout=FORM_PROJECT_CATEGORY_GOAL_EDIT["inp_monday"],
        )
        CustomEntry(
            master=self,
            tk_variable=self.min_tuesday_var,
            layout=FORM_PROJECT_CATEGORY_GOAL_EDIT["inp_tuesday"],
        )
        CustomEntry(
            master=self,
            tk_variable=self.min_wednesday_var,
            layout=FORM_PROJECT_CATEGORY_GOAL_EDIT["inp_wednesday"],
        )
        CustomEntry(
            master=self,
            tk_variable=self.min_thursday_var,
            layout=FORM_PROJECT_CATEGORY_GOAL_EDIT["inp_thursday"],
        )
        CustomEntry(
            master=self,
            tk_variable=self.min_friday_var,
            layout=FORM_PROJECT_CATEGORY_GOAL_EDIT["inp_friday"],
        )
        CustomEntry(
            master=self,
            tk_variable=self.min_saturday_var,
            layout=FORM_PROJECT_CATEGORY_GOAL_EDIT["inp_saturday"],
        )
        CustomEntry(
            master=self,
            tk_variable=self.min_sunday_var,
            layout=FORM_PROJECT_CATEGORY_GOAL_EDIT["inp_sunday"],
        )

        # Fill form
        if self.goal is not None:
            self.min_monday_var.set(self.goal.min_monday)
            self.min_tuesday_var.set(self.goal.min_tuesday)
            self.min_wednesday_var.set(self.goal.min_wednesday)
            self.min_thursday_var.set(self.goal.min_thursday)
            self.min_friday_var.set(self.goal.min_friday)
            self.min_saturday_var.set(self.goal.min_saturday)
            self.min_sunday_var.set(self.goal.min_sunday)

        # Submit form
        CustomButton(
            master=self,
            text="Save",
            command=self.save_entry,
            layout=FORM_PROJECT_CATEGORY_GOAL_EDIT["btn_save"],
        )

    def save_entry(self, *_args):
        """Read the values from the form fields, create a new Python
        object, and save it into the database.
        """
        new_goal = ProjectCategoryGoal(id=None)
        new_goal.project_category_id = self.category_id
        new_goal.project_category = ProjectCategoryService.get_by_id(
            self.db_session, self.category_id
        )

        new_goal.min_monday = self.min_monday_var.get()
        new_goal.min_tuesday = self.min_tuesday_var.get()
        new_goal.min_wednesday = self.min_wednesday_var.get()
        new_goal.min_thursday = self.min_thursday_var.get()
        new_goal.min_friday = self.min_friday_var.get()
        new_goal.min_saturday = self.min_saturday_var.get()
        new_goal.min_sunday = self.min_sunday_var.get()

        super().save_entry(new_goal)


#######################################################################
# CUSTOM WIDGETS
#######################################################################
class CustomButton(tb.Button):
    """A custom button widget which takes a layout dictionray which
    has to contain the following attributes:
    - row: int
    - col: int
    - sticky: str
    - padx: int or Tuple(int, int)
    - pady: int or Tuple(int, int)
    - width: int

    The meaning of those attributes can be looked up in the tkinter
    documentation.
    """

    def __init__(self, master, text, command, layout, bootstyle="default"):
        super().__init__(
            master=master,
            text=text,
            command=command,
            width=layout["width"],
            bootstyle=bootstyle,
        )
        self.grid(
            row=layout["row"],
            column=layout["col"],
            padx=layout["padx"],
            pady=layout["pady"],
        )


class CustomEntry(tb.Entry):
    """Same as CustomButton."""

    def __init__(self, master, tk_variable, layout):
        super().__init__(
            master=master,
            textvariable=tk_variable,
            width=layout["width"],
            font=layout["font"],
        )
        self.grid(
            row=layout["row"],
            column=layout["col"],
            padx=layout["padx"],
            pady=layout["pady"],
            sticky=layout["sticky"],
        )


class CustomScrolledText(ScrolledText):
    """Same as CustomButton."""

    def __init__(self, master, layout, autohide=True, **kwargs):
        super().__init__(
            master=master,
            height=layout["height"],
            autohide=autohide,
            width=layout["width"],
            font=layout["font"],
            wrap=tb.WORD,
            **kwargs,
        )
        self.grid(
            row=layout["row"],
            column=layout["col"],
            padx=layout["padx"],
            pady=layout["pady"],
            sticky=layout["sticky"],
        )

    def get_text(self) -> str:
        """Returns the content of the text widget and removes any
        trailing whitespace (or \\n).
        """
        return self.text.get(1.0, tb.END).rstrip()

    def set_text(self, new_text):
        self.clear()
        if new_text is not None:
            self.text.insert(1.0, new_text)
        else:
            self.text.insert(1.0, "")

    def clear(self) -> None:
        """Clears any input of the text widget."""
        self.text.delete(1.0, tb.END)


class CustomCombobox(tb.Combobox):
    """Same as CustomButton.

    Parameters
    ----------
    tk_key_var : ttkbootstrap.IntVar
        The tkinter variable to be updated with the key of the selected
        item.
    tk_value_var : ttkbootstrap.StringVar
        The tkinter variable to be updated with the value of the
        selected item.
    elements : dict(int: str)
        Expects a dictionary with key value pairs. The values will be
        displayed for selection, while both the key and value variables
        will be updated upon selection.
    """

    def __init__(
        self, master, tk_key_var, tk_value_var, layout, elements=None
    ):
        super().__init__(
            master=master,
            textvariable=tk_value_var,
            width=layout["width"],
            font=layout["font"],
            style="CustomCombobox",
        )
        self.grid(
            row=layout["row"],
            column=layout["col"],
            padx=layout["padx"],
            pady=layout["pady"],
            sticky=layout["sticky"],
        )

        tk_value_var.trace("w", self.select_handler)
        self.tk_key_var = tk_key_var
        self.elements = {v: k for k, v in elements.items()}

        if elements is not None:
            self["values"] = list(self.elements.keys())

    def select_handler(self, *_args):
        """Callback function for when an item is selected."""
        self.tk_key_var.set(self.elements[self.get()])
