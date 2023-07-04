import ttkbootstrap as tb
from ttkbootstrap.tableview import Tableview
from datetime import datetime
# Custom libraries
from src.components.TimeEntryForm import TimeEntryForm
from src.components.Timer import Timer
from ..controller.time_entry_service import TimeEntryService
from ..model.time_entry import TimeEntry


class TimeEntriesList(tb.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.build_components()

    def build_components(self):
        # Table
        self.columns = [
            'db_id',
            'Date',
            'Day',
            'Start',
            'Stop',
            'Pause',
            'Duration',
            'Project ID',
            'Project Name',
            'Activity ID',
            'Activity Name'
        ]
        hidden_columns_idx = [0, 7, 9]
        columns_idx_align_right = [3, 4, 5, 6]

        entries = TimeEntryService.get_all(self.app.session).all()
        row_data = [entry.to_list() for entry in entries]

        self.table = Tableview(self,
                               coldata=self.columns,
                               rowdata=row_data,
                               paginated=True,
                               autofit=True,
                               autoalign=True,
                               pagesize=50)
        for col_idx in hidden_columns_idx:
            self.table.hide_selected_column(cid=col_idx)
        for col_idx in columns_idx_align_right:
            self.table.align_column_right(cid=col_idx)
        self.table.sort_column_data(cid=1, sort=1)
        self.table.view.bind('<<TreeviewSelect>>', self.on_tb_tableview_select)
        self.table.grid(row=0, column=0, sticky='nsew', rowspan=3)

        # Right sidebar form
        self.te_form = TimeEntryForm(self, self.app)
        self.te_form.grid(row=0, column=1, sticky='n', padx=20)

        separator = tb.Separator(self)
        separator.grid(row=1, column=1, sticky='ew')

        self.timer = Timer(self, self.app)
        self.timer.grid(row=2, column=1, sticky='s', pady=30)       

    def on_tb_tableview_select(self, _):
        try:
            self.selected_iid = self.table.view.selection()[0]
            values = self.table.view.item(self.selected_iid, 'values')
            selected_te = TimeEntry.from_list(values)
            self.te_form.set_time_entry(selected_te)
        except IndexError:
            print('Index not found.')

    def add_entry(self, te: TimeEntry):
        #self.table.insert_row(0, te.to_list())
        #self.table.load_table_data()
        self.rebuild_table()
        self.app.stats_sidebar.update_goal_progress()

    def update_entry(self, te: TimeEntry):
        # Temporary database reload. TODO: Update tableview row.
        # self.table.view.item(self.selected_iid, values=te.to_list)
        self.rebuild_table()
        self.app.stats_sidebar.update_goal_progress()

    def rebuild_table(self):
        entries = TimeEntryService.get_all(self.app.session).all()
        row_data = [entry.to_list() for entry in entries]
        self.table.delete_rows()
        self.table.insert_rows(tb.END, row_data)
        self.table.load_table_data()

    def start_new_entry(self):
        self.te_form.form_for_new_entry()

    def resume_entry(self, curr_pause_duration):
        self.te_form.te_pause.delete(0, tb.END)
        self.te_form.te_pause.insert(
            0, str(curr_pause_duration).split('.', 2)[0]
        )

    def stop_entry(self, curr_duration):
        self.te_form.te_end.delete(0, tb.END)
        self.te_form.te_end.insert(0, datetime.now().strftime('%H:%M:%S'))

        self.te_form.te_duration['text'] = str(curr_duration).split('.', 2)[0]
