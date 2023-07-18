import ttkbootstrap as tb
from ttkbootstrap.tooltip import ToolTip
from tkinter import filedialog
from datetime import datetime, timedelta
from PIL import Image, ImageTk

import config.definitions as definitions
from ..controller.time_entry_service import TimeEntryService
from ..controller.time_controller import TimeController as tc
from ..model.time_entry import TimeEntry


class LeftSidebar(tb.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.config = parent.config
        self.app = app

        self.seconds_today = self.parent.parent.sc.total_time_today()

        self.__build_gui_components()
        self.update_achievements()
        self.update_goal_progress()

    def __build_gui_components(self):
        self.lbl_progress = tb.Label(
            self,
            text=tc.timedelta_to_string(timedelta(seconds=self.seconds_today)),
            font=("Helvetica", 24, "bold"),
        )
        self.lbl_progress.pack(padx=10, pady=25)

        # Achievements
        frm_achievements = tb.Frame(self)
        frm_achievements.pack(padx=10, pady=10, fill="x")

        self.lbl_header_achievements = tb.Label(
            frm_achievements,
            text="Achievements",
            font=(None, 20, "bold"),
            justify="left",
        )

        self.frm_medals = tb.Frame(frm_achievements)

        bronze_img_orig = Image.open(
            f"{definitions.APP_ROOT_DIR}/assets/icons/medal-bronze.png"
        ).resize((64, 64))
        bronze_img_tk = ImageTk.PhotoImage(bronze_img_orig)
        self.lbl_medal_bronze = tb.Label(self.frm_medals, image=bronze_img_tk)
        self.lbl_medal_bronze.photo = bronze_img_tk
        txt = f"You worked for more than {tc.seconds_to_string(definitions.MEDAL_TH_BRONZE)}!"
        ToolTip(self.lbl_medal_bronze, text=txt)

        silver_img_orig = Image.open(
            f"{definitions.APP_ROOT_DIR}/assets/icons/medal-silver.png"
        ).resize((64, 64))
        silver_img_tk = ImageTk.PhotoImage(silver_img_orig)
        self.lbl_medal_silver = tb.Label(self.frm_medals, image=silver_img_tk)
        self.lbl_medal_silver.photo = silver_img_tk
        txt = f"You worked for more than {tc.seconds_to_string(definitions.MEDAL_TH_SILVER)}!"
        ToolTip(self.lbl_medal_silver, text=txt)

        gold_img_orig = Image.open(
            f"{definitions.APP_ROOT_DIR}/assets/icons/medal-gold.png"
        ).resize((64, 64))
        gold_img_tk = ImageTk.PhotoImage(gold_img_orig)
        self.lbl_medal_gold = tb.Label(self.frm_medals, image=gold_img_tk)
        self.lbl_medal_gold.photo = gold_img_tk
        txt = f"You worked for more than {tc.seconds_to_string(definitions.MEDAL_TH_GOLD)}!"
        ToolTip(self.lbl_medal_gold, text=txt)

        # Project category goals
        goals_section_heading = tb.Label(
            self,
            text=datetime.today().strftime("%A"),
            font=(None, 20, "bold"),
            justify="left",
        )
        goals_section_heading.pack(padx=10, pady=0, fill="x")

        goals = self.parent.parent.pcgsc.get_active_goals()
        self.goal_dict = {}

        weekday = datetime.today().weekday()
        for goal in goals:
            if goal.get_weekday_minute_goal(weekday) > 0:
                progress_card = ProjectCategoryProgressCard(
                    self, self.app, goal
                )
                progress_card.pack(fill="x", padx=10, pady=10)
                self.goal_dict[goal.project_category_id] = {
                    "goal": goal,
                    "progress_card": progress_card,
                }

        # Versioning
        msg_user = definitions.APP_VERSION
        lbl_username = tb.Label(self, text=msg_user)
        lbl_username.pack(side="bottom", pady=10)

        # Import/Export buttons
        frame_file_operations = tb.Frame(self)
        frame_file_operations.pack(side="bottom", padx=10, pady=10)

        btn_open_db_file = tb.Button(
            frame_file_operations,
            text="Import",
            command=self.btn_import_handler,
        )
        btn_open_db_file.grid(row=0, column=0, padx=10)

        btn_export_db_file = tb.Button(
            frame_file_operations,
            text="Export",
            command=self.btn_export_handler,
        )
        btn_export_db_file.grid(row=0, column=1, padx=10)

    def update_total_time(self, added_duration):
        self.total_time = (
            timedelta(seconds=self.parent.parent.sc.total_time_today())
            + added_duration
        )
        self.lbl_progress["text"] = tc.timedelta_to_string(self.total_time)

    def update_achievements(self):
        if self.seconds_today >= (120 * 60):
            self.lbl_header_achievements.pack(
                side="top", padx=10, pady=0, fill="x"
            )
            self.frm_medals.pack()
            self.lbl_medal_bronze.pack(side="left")
        if self.seconds_today >= (240 * 60):
            self.lbl_medal_silver.pack(side="left")
        if self.seconds_today >= (360 * 60):
            self.lbl_medal_gold.pack(side="left")

    def update_goal_progress(self):
        """Update the progress value for all active project category
        goals iteratively.
        """
        time_entries = self.parent.parent.pcgsc.get_time_entries_per_category()
        goal_progress_dict = {}
        for category_id in self.goal_dict.keys():
            goal_progress_dict[category_id] = 0

        for category_id, entry in time_entries:
            if category_id in self.goal_dict:
                goal_progress_dict[category_id] += entry.get_duration_minutes()

        for category_id in self.goal_dict.keys():
            current_progress = int(goal_progress_dict[category_id])
            self.goal_dict[category_id]["progress_card"].update_progress(
                current_progress
            )

    def btn_import_handler(self):
        filename = filedialog.askopenfilename(
            title="Import Database",
            defaultextension=".db",
            initialdir="~",
            filetypes=(("db files", "*.db"), ("all files", "*.*")),
        )
        self.app.file_controller.import_database_file(filename)

    def btn_export_handler(self):
        filename = filedialog.asksaveasfilename(
            title="Export Database",
            confirmoverwrite=True,
            defaultextension=".db",
            initialdir="~",
            filetypes=[("SQLite Database", "*.db")],
            initialfile="backup.db",
        )
        self.app.file_controller.export_database_file(filename)


class ProjectCategoryProgressCard(tb.Frame):
    """
    Parameters
    ----------
    weekday: int
        The weekday for which to display the progress. From 0 (Monday)
        to 6 (Sunday).
    """

    def __init__(self, parent, app, goal):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.goal = goal
        self.goal_progress = 0
        weekday = datetime.today().weekday()
        self.goal_max = self.goal.get_weekday_minute_goal(weekday)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.__build_gui_components()

    def __build_gui_components(self):
        lbl_goal = tb.Label(
            self, text=self.goal.project_category.name, justify="left"
        )
        lbl_goal.grid(row=0, column=0, sticky="w")
        self.lbl_goal_progress = tb.Label(
            self,
            text=f"{self.goal_progress}/{self.goal_max}m",
            justify="right",
        )
        self.lbl_goal_progress.grid(row=0, column=1, sticky="e")
        self.fg_goal_progress = tb.Floodgauge(self, maximum=self.goal_max)
        self.fg_goal_progress.grid(row=1, column=0, columnspan=2, sticky="ew")

    def update_progress(self, progress_value: int):
        if progress_value > self.goal_max:
            self.fg_goal_progress.configure(bootstyle="success")
        progress_str = f"{progress_value}/{self.goal_max}m"
        self.lbl_goal_progress["text"] = progress_str
        self.fg_goal_progress.configure(value=progress_value)
