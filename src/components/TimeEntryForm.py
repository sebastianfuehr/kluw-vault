import ttkbootstrap as tb
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.scrolled import ScrolledText, ScrolledFrame
from datetime import datetime, timedelta
# Custom modules
from ..model.time_entry import TimeEntry
from ..model.project import Project
from ..model.activity import Activity
from ..controller.time_entry_service import TimeEntryService
from ..controller.project_service import ProjectService
from ..controller.activity_service import ActivityService


class TimeEntryForm(tb.Frame):
    """A form for editing and adding new time entries.
    """

    def __init__(self, parent, app, new_entry_var):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.new_entry_var = new_entry_var

        self.entry_font = ('Helvetica', 16)

        self.build_form_components()
        self.set_time_entry(None)

    def build_form_components(self):
        """Creates the GUI widgets for this component.
        """
        frm_padx = 10
        lbl_pax = 10
        field_padx = 0
        inp_width = 14

        frame_heading = tb.Frame(self)
        frame_heading.pack(fill='x', padx=frm_padx, pady=10)

        lbl_heading = tb.Label(
            frame_heading, text='Time Entry', font=(None, 24, 'bold')
        )
        lbl_heading.pack(side='left')

        self.btn_new_entry = tb.Button(
            frame_heading,
            text='New',
            bootstyle='success',
            command=self.__select_handler_new_entry
        )
        self.btn_new_entry.pack(side='right')

        scr_frame = ScrolledFrame(self, padding=0, width=315)
        scr_frame.pack(expand=True, fill='both', padx=0)
        scr_frame.grid_columnconfigure(1, weight=1)

        lbl_te_date = tb.Label(scr_frame, text='Date:')
        lbl_te_date.grid(column=0, row=1, sticky='w', padx=lbl_pax, pady=5)
        self.te_date = tb.Entry(
            scr_frame, width=inp_width, font=self.entry_font, justify='center'
        )
        self.te_date.grid(column=1, row=1, sticky='e', padx=field_padx, pady=5)

        lbl_te_weekday = tb.Label(scr_frame, text='Day:')
        lbl_te_weekday.grid(column=0, row=2, sticky='w', padx=lbl_pax, pady=5)
        self.te_weekday = tb.Label(scr_frame, width=inp_width, anchor='center')
        self.te_weekday.grid(column=1, row=2, sticky='e', padx=field_padx, pady=5)
        self.te_weekday['text'] = datetime.today().strftime('%a')

        lbl_te_start = tb.Label(scr_frame, text='Start:')
        lbl_te_start.grid(column=0, row=3, sticky='w', padx=lbl_pax, pady=5)
        self.te_start = tb.Entry(
            scr_frame, font=self.entry_font, width=inp_width, justify='center'
        )
        self.te_start.grid(column=1, row=3, sticky='e', padx=field_padx, pady=5)

        lbl_te_end = tb.Label(scr_frame, text='End:')
        lbl_te_end.grid(column=0, row=4, sticky='w', padx=lbl_pax, pady=5)
        self.te_end = tb.Entry(
            scr_frame, font=self.entry_font, width=inp_width, justify='center'
        )
        self.te_end.grid(column=1, row=4, sticky='e', padx=field_padx, pady=5)

        lbl_te_pause = tb.Label(scr_frame, text='Pause:')
        lbl_te_pause.grid(column=0, row=5, sticky='w', padx=lbl_pax, pady=5)
        self.te_pause = tb.Entry(
            scr_frame, font=self.entry_font, width=inp_width, justify='center'
        )
        self.te_pause.grid(column=1, row=5, sticky='e', padx=field_padx, pady=5)

        lbl_te_duration = tb.Label(scr_frame, text='Duration:')
        lbl_te_duration.grid(column=0, row=6, sticky='w', padx=lbl_pax, pady=5)
        self.te_duration = tb.Label(scr_frame, width=inp_width, anchor='center')
        self.te_duration.grid(column=1, row=6, sticky='e', padx=field_padx, pady=5)
        self.te_duration['text'] = '00:00:00'

        # Project combobox
        projects = ProjectService.get_all(self.app.session).all()
        project_names = [project.name for project in projects]
        if len(project_names) == 0:
            init_proj_name = None
        else:
            init_proj_name = project_names[0]
        self.selected_project = tb.StringVar(value=init_proj_name)
        self.selected_project.trace('w', self.__populate_activities_list)

        lbl_te_project = tb.Label(scr_frame, text='Project:')
        lbl_te_project.grid(column=0, row=7, sticky='w', padx=lbl_pax, pady=5)
        self.te_project = tb.Combobox(
            scr_frame,
            textvariable=self.selected_project,
            font=self.entry_font,
            width=12,
            justify='right'
        )
        self.te_project.grid(column=1, row=7, sticky='e', padx=field_padx, pady=5)
        self.te_project['values'] = project_names

        # Activity combobox
        self.selected_activity = tb.StringVar()
        lbl_te_activity = tb.Label(scr_frame, text='Activity:')
        lbl_te_activity.grid(column=0, row=8, sticky='w', padx=lbl_pax, pady=5)
        self.te_activity = tb.Combobox(
            scr_frame,
            textvariable=self.selected_activity,
            font=self.entry_font,
            width=12,
            justify='right'
        )
        self.te_activity.grid(column=1, row=8, sticky='e', padx=field_padx, pady=5)
        self.__populate_activities_list()

        self.te_alone_var = tb.IntVar(value=1)
        lbl_te_alone = tb.Label(scr_frame, text='Alone:')
        lbl_te_alone.grid(column=0, row=9, sticky='w', padx=lbl_pax, pady=5)
        self.te_alone = tb.Checkbutton(
            scr_frame, variable=self.te_alone_var, bootstyle='round-toggle'
        )
        self.te_alone.grid(column=1, row=9, padx=field_padx, pady=5)

        lbl_te_tags = tb.Label(scr_frame, text='Tags:')
        lbl_te_tags.grid(column=0, row=10, sticky='nw', padx=lbl_pax, pady=5)
        self.te_tags = ScrolledText(
            scr_frame,
            font=self.entry_font,
            width=inp_width,
            height=3,
            autohide=True
        )
        self.te_tags.grid(
            column=1, row=10, sticky='e', padx=field_padx, pady=5
        )
        ToolTip(self.te_tags, text='One tag per line.')

        lbl_te_comment = tb.Label(scr_frame, text='Comment:')
        lbl_te_comment.grid(
            column=0, row=11, columnspan=2, sticky='w', padx=lbl_pax, pady=5
        )
        self.te_comment = ScrolledText(
            scr_frame,
            font=self.entry_font,
            width=inp_width,
            height=3,
            autohide=True
        )
        self.te_comment.grid(
            column=0,
            row=12,
            columnspan=2,
            sticky='ew',
            padx=(10, 0),
            pady=5
        )

        # Button
        self.btn_save_entry = tb.Button(
            scr_frame,
            text='Save',
            command=self.save_entry,
            width=14)
        self.btn_save_entry.grid(
            column=0,
            row=13,
            columnspan=2,
            padx=10,
            pady=20
        )

    def __populate_activities_list(self, *args):
        self.selected_activity.set('')
        project_name = self.selected_project.get()
        if project_name == '':
            self.te_activity['values'] = []
        else:
            project = ProjectService.get_project_by_name(
                self.app.session,
                project_name
            )
            activity_names = [activity.name for activity in project.activities]
            self.te_activity['values'] = activity_names
            if len(activity_names) > 0:
                self.selected_activity.set(activity_names[0])

    def __select_handler_new_entry(self, *args):
        if self.new_entry_var.get():
            self.new_entry_var.set(False)
        else:
            self.new_entry_var.set(True)
        self.form_for_new_entry()

    def form_for_new_entry(self):
        """Callback wrapper for set_tim_entry(None).
        """
        self.set_time_entry(None)
        if self.new_entry_var.get():
            self.btn_new_entry.configure(bootstyle='danger', text='Cancel')
        else:
            self.btn_new_entry.configure(bootstyle='success', text='New')

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

            self.selected_project.set('')
            self.selected_activity.set('')

            self.te_alone_var.set(1)
            self.te_tags.text.delete('1.0', tb.END)
            self.te_comment.text.delete('1.0', tb.END)
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

            self.selected_project.set(self.time_entry.get_project_name())
            self.selected_activity.set(self.time_entry.get_activity_name())

            self.te_alone_var.set(int(self.time_entry.alone == 'True'))

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
        new_entry.start = datetime.strptime(f'{date} {self.te_start.get()}',
                                            '%Y-%m-%d %H:%M:%S')
        new_entry.stop = datetime.strptime(f'{date} {self.te_end.get()}',
                                           '%Y-%m-%d %H:%M:%S')
        pause_datetime = datetime.strptime(self.te_pause.get(), '%H:%M:%S')
        pause_duration = timedelta(
            hours=pause_datetime.hour,
            minutes=pause_datetime.minute,
            seconds=pause_datetime.second
        )
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
