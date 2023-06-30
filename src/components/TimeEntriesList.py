import ttkbootstrap as tb
from ttkbootstrap.tableview import Tableview
# Custom libraries
from src.components.TimeEntryForm import TimeEntryForm
from ..controller.time_entry_service import TimeEntryService
from ..model.time_entry import TimeEntry


class TimeEntriesList(tb.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app

        self.build_components()

    def build_components(self):
        # Columns
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
        self.table.view.bind('<<TreeviewSelect>>', self.on_tb_tableview_select)
        self.table.pack(side='left', expand=True, fill='both')

        # Right sidebar form
        self.te_form = TimeEntryForm(self, self.app)
        self.te_form.pack(side='right', fill='y', padx=10, pady=10)

        """
        # Tksheets
        sheet = tksheet.Sheet(self,
                              theme='dark green',
                              header=headers)
        sheet.pack(fill="both")
        sheet.set_sheet_data(row_data)
        sheet.enable_bindings(("single_select",
                               "row_select",
                               "arrowkeys",
                               "column_width_resize",
                               "row_height_resize",
                               "copy",
                               "edit_cell"))
        sheet.readonly_columns(columns=[1,5], readonly=True)
        sheet.align_columns(columns=[3,4,5,], align="e", align_header=False)
        """

    def on_tb_tableview_select(self, _):
        try:
            self.selected_iid = self.table.view.selection()[0]
            values = self.table.view.item(self.selected_iid, 'values')
            print(f'Selected {self.selected_iid}: {values}')
            selected_te = TimeEntry.from_list(values)
            self.te_form.set_time_entry(selected_te)
        except IndexError:
            print('Index not found.')

    def add_entry(self, te: TimeEntry):
        self.table.insert_row(tb.END, te.to_list())
        self.table.load_table_data()

    def update_entry(self, te: TimeEntry):
        # Temporary database reload. TODO: Update tableview row.
        # self.table.view.item(self.selected_iid, values=te.to_list)
        self.rebuild_table()

    def rebuild_table(self):
        entries = TimeEntryService.get_all(self.app.session).all()
        row_data = [entry.to_list() for entry in entries]
        self.table.delete_rows()
        self.table.insert_rows(tb.END, row_data)
        self.table.load_table_data()
