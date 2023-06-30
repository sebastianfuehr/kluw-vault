import ttkbootstrap as tb
from datetime import datetime
# Custom modules
from ..model.time_entry import TimeEntry
from ..controller.time_entry_service import TimeEntryService


class TimeEntryForm(tb.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app

        self.build_form_components()
        self.set_time_entry(None)

    def build_form_components(self):
        lbl_te_date = tb.Label(self, text='Date:')
        lbl_te_date.grid(column=0, row=0)
        self.te_date = tb.DateEntry(self, dateformat='%Y-%m-%d')
        self.te_date.grid(column=1, row=0)

        lbl_te_weekday = tb.Label(self, text='Day:')
        lbl_te_weekday.grid(column=0, row=1)
        self.te_weekday = tb.Label(self)
        self.te_weekday.grid(column=1, row=1)
        self.te_weekday['text'] = datetime.today().strftime('%a')

        lbl_te_start = tb.Label(self, text='Start:')
        lbl_te_start.grid(column=0, row=2)
        self.te_start = tb.Entry(self)
        self.te_start.grid(column=1, row=2)

        lbl_te_end = tb.Label(self, text='End:')
        lbl_te_end.grid(column=0, row=3)
        self.te_end = tb.Entry(self)
        self.te_end.grid(column=1, row=3)

        lbl_te_pause = tb.Label(self, text='Pause:')
        lbl_te_pause.grid(column=0, row=4)
        self.te_pause = tb.Entry(self)
        self.te_pause.grid(column=1, row=4)

        lbl_te_duration = tb.Label(self, text='Duration:')
        lbl_te_duration.grid(column=0, row=5)
        self.te_duration = tb.Label(self)
        self.te_duration.grid(column=1, row=5)
        self.te_duration['text'] = '00:00:00'

        self.btn_save_entry = tb.Button(self,
                                        text='Save',
                                        command=self.save_entry)
        self.btn_save_entry.grid(column=0,
                                 row=6,
                                 columnspan=2)

        self.btn_new_entry = tb.Button(self,
                                       text='New',
                                       bootstyle='success',
                                       command=self.empty_form)
        self.btn_new_entry.grid(column=0,
                                row=7,
                                columnspan=2)

    def empty_form(self):
        self.set_time_entry(None)

    def set_time_entry(self, time_entry: TimeEntry):
        print('set_time_entry')
        self.time_entry = time_entry
        self.__populate_fields()

    def __populate_fields(self):
        if self.time_entry is None:
            # Rest all fields
            print('Reset form fields.')
            self.te_date.entry.delete(0, tb.END)
            self.te_weekday['text'] = ''
            self.te_start.delete(0, tb.END)
            self.te_end.delete(0, tb.END)
            self.te_pause.delete(0, tb.END)
            self.te_duration['text'] = '0:00:00'
        else:
            print(f'Populate fields with {self.time_entry.to_list()}')
            # Fill form fields with time entry values
            self.te_date.entry.delete(0, tb.END)
            self.te_date.entry.insert(0, self.time_entry.get_date())

            self.te_weekday['text'] = self.time_entry.get_weekday()

            self.te_start.delete(0, tb.END)
            self.te_start.insert(0, self.time_entry.get_start_time())

            self.te_end.delete(0, tb.END)
            new_end_time = self.time_entry.get_end_time()
            if new_end_time is not None:
                self.te_end.insert(0, new_end_time)

            self.te_pause.delete(0, tb.END)
            self.te_pause.insert(0, self.time_entry.get_pause_seconds())

            self.te_duration['text'] = self.time_entry.get_duration_timedelta()

    def save_entry(self):
        if self.time_entry is None:
            new_entry = TimeEntry(None)
        else:
            new_entry = self.time_entry

        date = self.te_date.entry.get()
        new_entry.start = datetime.strptime(f'{date} {self.te_start.get()}',
                                            '%Y-%m-%d %H:%M:%S')
        new_entry.stop = datetime.strptime(f'{date} {self.te_end.get()}',
                                           '%Y-%m-%d %H:%M:%S')
        new_entry.pause = int(self.te_pause.get())
        TimeEntryService.merge(self.app.session, new_entry)

        if self.time_entry is None:
            self.parent.add_entry(new_entry=new_entry)
        else:
            self.parent.update_entry(te=new_entry)
