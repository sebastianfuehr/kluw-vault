import ttkbootstrap as tb
from datetime import datetime, timedelta
# Custom modules
from ..model.time_entry import TimeEntry
from ..model.project import Project
from ..model.activity import Activity
from ..controller.time_entry_service import TimeEntryService
from ..controller.project_service import ProjectService
from ..controller.activity_service import ActivityService


class TimeEntryForm(tb.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app

        self.entry_font = ('Helvetica', 16)

        self.build_form_components()
        self.set_time_entry(None)

    def build_form_components(self):
        frame_heading = tb.Frame(self)
        frame_heading.grid(row=0, column=0, columnspan=2, sticky='ew', pady=20)

        lbl_heading = tb.Label(frame_heading, text='Time Entry', font=(None, 24, 'bold'))
        lbl_heading.pack(side='left')

        self.btn_new_entry = tb.Button(frame_heading,
                                       text='New',
                                       bootstyle='success',
                                       command=self.form_for_new_entry)
        self.btn_new_entry.pack(side='right')

        lbl_te_date = tb.Label(self, text='Date:')
        lbl_te_date.grid(column=0, row=1, sticky='w', padx=10, pady=5)
        self.te_date = tb.Entry(self, font=self.entry_font, width=14, justify='center')
        self.te_date.grid(column=1, row=1, sticky='e', padx=10, pady=5)

        lbl_te_weekday = tb.Label(self, text='Day:')
        lbl_te_weekday.grid(column=0, row=2, sticky='w', padx=10, pady=5)
        self.te_weekday = tb.Label(self, width=14, anchor='center')
        self.te_weekday.grid(column=1, row=2, sticky='e', padx=10, pady=5)
        self.te_weekday['text'] = datetime.today().strftime('%a')

        lbl_te_start = tb.Label(self, text='Start:')
        lbl_te_start.grid(column=0, row=3, sticky='w', padx=10, pady=5)
        self.te_start = tb.Entry(self, font=self.entry_font, width=14, justify='center')
        self.te_start.grid(column=1, row=3, sticky='e', padx=10, pady=5)

        lbl_te_end = tb.Label(self, text='End:')
        lbl_te_end.grid(column=0, row=4, sticky='w', padx=10, pady=5)
        self.te_end = tb.Entry(self, font=self.entry_font, width=14, justify='center')
        self.te_end.grid(column=1, row=4, sticky='e', padx=10, pady=5)

        lbl_te_pause = tb.Label(self, text='Pause:')
        lbl_te_pause.grid(column=0, row=5, sticky='w', padx=10, pady=5)
        self.te_pause = tb.Entry(self, font=self.entry_font, width=14, justify='center')
        self.te_pause.grid(column=1, row=5, sticky='e', padx=10, pady=5)

        lbl_te_duration = tb.Label(self, text='Duration:')
        lbl_te_duration.grid(column=0, row=6, sticky='w', padx=10, pady=5)
        self.te_duration = tb.Label(self, width=14, anchor='center')
        self.te_duration.grid(column=1, row=6, sticky='e', padx=10, pady=5)
        self.te_duration['text'] = '00:00:00'

        # Project combobox
        projects = ProjectService.get_all(self.app.session).all()
        project_names = [project.name for project in projects]
        if len(project_names) == 0:
            init_proj_name = None
        else:
            init_proj_name = project_names[0]
        self.selected_project = tb.StringVar(value=init_proj_name)

        lbl_te_project = tb.Label(self, text='Project:')
        lbl_te_project.grid(column=0, row=7, sticky='w', padx=10, pady=5)
        self.te_project = tb.Combobox(self,
                                      textvariable=self.selected_project,
                                      font=self.entry_font,
                                      width=12,
                                      justify='right')
        self.te_project.grid(column=1, row=7, sticky='e', padx=10, pady=5)
        self.te_project['values'] = project_names

        # Activity combobox
        activities = ActivityService.get_all(self.app.session).all()
        activity_names = [activity.name for activity in activities]
        if len(activity_names) == 0:
            init_act_name = None
        else:
            init_act_name = activity_names[0]
        self.selected_activity = tb.StringVar(value=init_act_name)

        lbl_te_activity = tb.Label(self, text='Activity:')
        lbl_te_activity.grid(column=0, row=8, sticky='w', padx=10, pady=5)
        self.te_activity = tb.Combobox(self,
                                       textvariable=self.selected_activity,
                                       font=self.entry_font,
                                       width=12,
                                       justify='right')
        self.te_activity.grid(column=1, row=8, sticky='e', padx=10, pady=5)
        self.te_activity['values'] = activity_names

        # Button
        self.btn_save_entry = tb.Button(self,
                                        text='Save',
                                        command=self.save_entry,
                                        width=14)
        self.btn_save_entry.grid(column=0,
                                 row=9,
                                 columnspan=2,
                                 padx=10,
                                 pady=20)

    def form_for_new_entry(self):
        self.set_time_entry(None)

    def set_time_entry(self, time_entry: TimeEntry):
        self.time_entry = time_entry
        self.__populate_fields()

    def __populate_fields(self):
        if self.time_entry is None:
            # Rest all fields
            self.te_date.delete(0, tb.END)
            self.te_date.insert(0, datetime.now().date())

            self.te_weekday['text'] = datetime.now().strftime('%a')

            self.te_start.delete(0, tb.END)
            self.te_start.insert(0, datetime.now().strftime('%H:%M:%S'))

            self.te_end.delete(0, tb.END)
            self.te_end.insert(0, datetime.now().strftime('%H:%M:%S'))

            self.te_pause.delete(0, tb.END)
            self.te_pause.insert(0, '0:00:00')

            # TODO: Extra method for calculating the duration outside of the
            # time entry instance
            self.te_duration['text'] = '0:00:00'
        else:
            # Fill form fields with time entry values
            self.te_date.delete(0, tb.END)
            self.te_date.insert(0, self.time_entry.get_date())

            self.te_weekday['text'] = self.time_entry.get_weekday()

            self.te_start.delete(0, tb.END)
            self.te_start.insert(0, self.time_entry.get_start_time())

            self.te_end.delete(0, tb.END)
            new_end_time = self.time_entry.get_end_time()
            if new_end_time is not None:
                self.te_end.insert(0, new_end_time)

            self.te_pause.delete(0, tb.END)
            self.te_pause.insert(0, self.time_entry.get_pause_timedelta())

            self.te_duration['text'] = self.time_entry.get_duration_timedelta()

    def save_entry(self):
        if self.time_entry is None:
            new_entry = TimeEntry(None)
        else:
            new_entry = self.time_entry

        date = self.te_date.get()
        new_entry.start = datetime.strptime(f'{date} {self.te_start.get()}',
                                            '%Y-%m-%d %H:%M:%S')
        new_entry.stop = datetime.strptime(f'{date} {self.te_end.get()}',
                                           '%Y-%m-%d %H:%M:%S')
        pause_datetime = datetime.strptime(self.te_pause.get(), '%H:%M:%S')
        pause_duration = timedelta(hours=pause_datetime.hour,
                                   minutes=pause_datetime.minute,
                                   seconds=pause_datetime.second)
        new_entry.pause = int(pause_duration.total_seconds())
        proj_name = self.selected_project.get()
        new_entry.project_id = ProjectService.get_project_by_name(
            self.app.session,
            proj_name
        ).id
        new_entry.project = Project(
            id=new_entry.project_id,
            name=proj_name
        )
        activity_name = self.selected_activity.get()
        new_entry.activity_id = ActivityService.get_activity_id(
            self.app.session,
            activity_name,
            new_entry.project_id
        ).id
        new_entry.activity = Activity(
            id=new_entry.activity_id,
            name=activity_name
        )
        TimeEntryService.merge(self.app.session, new_entry)

        if self.time_entry is None:
            self.parent.add_entry(te=new_entry)
        else:
            self.parent.update_entry(te=new_entry)
