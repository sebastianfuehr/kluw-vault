import ttkbootstrap as tb
from tkinter import filedialog
from datetime import datetime, timedelta

from ..controller.time_entry_service import TimeEntryService
from ..controller.time_controller import TimeController as tc
from ..model.time_entry import TimeEntry
from src.components.ProjectCategoryProgressCard import ProjectCategoryProgressCard


class LeftSidebar(tb.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.config = parent.config
        self.app = app

        seconds_today = self.parent.parent.sc.total_time_today()
        self.lbl_progress = tb.Label(
            self,
            text=str(timedelta(seconds=seconds_today)),
            font=('Helvetica', 16, 'bold'))
        self.lbl_progress.pack(padx=10, pady=10)

        # Project category goals
        goals = self.parent.parent.pcgsc.get_goal_list(weekday=datetime.today().weekday())
        self.goal_dict = {}

        for goal in goals:
            progress_card = ProjectCategoryProgressCard(self, self.app, goal)
            progress_card.pack(fill='x', padx=10, pady=10)
            self.goal_dict[goal.project_category_id] = {
                'goal': goal,
                'progress_card': progress_card
            }

        self.update_goal_progress()

        msg_user = f"Currently logged in as {self.config['User']['last_login_username']}"
        lbl_username = tb.Label(self, text=msg_user)
        lbl_username.pack(side="bottom")

        frame_file_operations = tb.Frame(self)
        frame_file_operations.pack(side='bottom', padx=10, pady=10)

        btn_open_db_file = tb.Button(
            frame_file_operations,
            text='Import',
            command=self.btn_import_handler
        )
        btn_open_db_file.grid(row=0, column=0, padx=10)

        btn_export_db_file = tb.Button(
            frame_file_operations,
            text='Export',
            command=self.btn_export_handler
        )
        btn_export_db_file.grid(row=0, column=1, padx=10)

    def update_total_time(self, added_duration):
        total_time = timedelta(seconds=self.parent.parent.sc.total_time_today()) + added_duration
        self.lbl_progress['text'] = tc.timedelta_to_string(total_time)

    def update_goal_progress(self):
        print('update_goal_progress')
        time_entries = self.parent.parent.pcgsc.get_time_entries_per_category()
        goal_progress_dict = {}
        for category_id in self.goal_dict.keys():
            goal_progress_dict[category_id] = 0

        for category_id, te in time_entries:
            goal_progress_dict[category_id] += te.get_duration_minutes()

        for category_id in self.goal_dict.keys():
            current_progress = int(goal_progress_dict[category_id])
            self.goal_dict[category_id]['progress_card'].update_progress(current_progress)

    def btn_import_handler(self):
        filename = filedialog.askopenfilename(
            title='Import Database',
            defaultextension='.db',
            initialdir='~',
            filetypes=(('db files', '*.db'), ('all files', '*.*'))
        )
        self.app.file_controller.import_database_file(filename)

    def btn_export_handler(self):
        filename = filedialog.asksaveasfilename(
            title='Export Database',
            confirmoverwrite=True,
            defaultextension='.db',
            initialdir='~',
            filetypes=[('SQLite Database', '*.db')],
            initialfile='backup.db'
        )
        self.app.file_controller.export_database_file(filename)
