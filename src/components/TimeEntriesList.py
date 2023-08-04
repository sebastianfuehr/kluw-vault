from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import ttkbootstrap as tb
from ttkbootstrap.tableview import Tableview

# Custom libraries
from src.components.forms import TimeEntryForm
from src.components.timer import Timer

from ..controller.time_entry_service import TimeEntryService
from ..model.time_entry import TimeEntry

if TYPE_CHECKING:
    from datetime import timedelta

    from app import App


class TimeEntriesList(tb.Frame):  # type: ignore
    def __init__(self, parent: tb.Frame, app: "App") -> None:
        super().__init__(parent)
        self.parent = parent
        self.app = app

        self.new_entry = tb.BooleanVar(self, False)
        self.new_entry.trace("w", self.__handle_new_entry_panel)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.build_components()

    def build_components(self) -> None:
        # Table
        self.columns = [
            "db_id",
            "Date",
            "Day",
            "Start",
            "Stop",
            "Pause",
            "Duration",
            "Project ID",
            "Project Name",
            "Activity ID",
            "Activity Name",
            "Alone",
            "Tags",
            "Comment",
        ]
        hidden_columns_idx = [0, 7, 9]
        columns_idx_align_right = [3, 4, 5, 6]

        entries = TimeEntryService.get_all(self.app.session).all()
        row_data = [entry.to_list() for entry in entries]

        self.table = Tableview(
            self,
            coldata=self.columns,
            rowdata=row_data,
            paginated=True,
            autofit=True,
            autoalign=True,
            pagesize=50,
        )
        for col_idx in hidden_columns_idx:
            self.table.hide_selected_column(cid=col_idx)
        for col_idx in columns_idx_align_right:
            self.table.align_column_right(cid=col_idx)
        self.table.sort_column_data(cid=1, sort=1)
        self.table.view.bind("<<TreeviewSelect>>", self.on_tb_tableview_select)
        self.table.grid(row=0, column=0, sticky="nsew", rowspan=3)

        self.frm_new_entry = tb.Frame(self)
        self.frm_new_entry.grid_columnconfigure(0, weight=1)
        self.frm_new_entry.grid_rowconfigure((0, 3), weight=1)
        lbl_new_entry = tb.Label(
            self.frm_new_entry, text="New Time Entry", font=(None, 18)
        )
        lbl_new_entry.grid(row=1, column=0)
        lbl_new_entry_description = tb.Label(
            self.frm_new_entry,
            text="You are currently creating a new time entry or the timer is running.",
            foreground="#a8a8a8",
        )
        lbl_new_entry_description.grid(row=2, column=0, pady=(10, 0))

        sep_vertical = tb.Separator(self, orient="vertical")
        sep_vertical.grid(row=0, column=1, sticky="ns", rowspan=3)

        # Right sidebar form
        self.te_form = TimeEntryForm(self, self.app, self.new_entry)
        self.te_form.grid(row=0, column=2, sticky="nsew")

        separator = tb.Separator(self)
        separator.grid(row=1, column=2, sticky="ew")

        self.timer = Timer(self, self.app, self.new_entry)
        self.timer.grid(row=2, column=2, sticky="s", pady=30)

    def on_tb_tableview_select(self, *_args: int) -> None:
        try:
            self.selected_iid = self.table.view.selection()[0]
            values = self.table.view.item(self.selected_iid, "values")
            selected_te: TimeEntry = TimeEntry.from_list(values)
            self.te_form.set_time_entry(selected_te)
        except IndexError:
            print("Index not found.")

    def __handle_new_entry_panel(self, *args: int) -> None:
        """Overlay the time entry tabel with an information panel,
        while a new time entry is being created or the timer is
        running.
        """
        if self.new_entry.get():
            self.table.grid_forget()
            self.frm_new_entry.grid(row=0, column=0, sticky="nsew", rowspan=3)
        else:
            self.frm_new_entry.grid_forget()
            self.table.grid(row=0, column=0, sticky="nsew", rowspan=3)

    def add_entry(self, te: TimeEntry) -> None:
        # self.table.insert_row(0, te.to_list())
        # self.table.load_table_data()
        self.rebuild_table()
        self.app.stats_sidebar.update_goal_progress()

    def update_entry(self, te: TimeEntry) -> None:
        # Temporary database reload. TODO: Update tableview row.
        # self.table.view.item(self.selected_iid, values=te.to_list)
        self.rebuild_table()
        self.app.stats_sidebar.update_goal_progress()

    def rebuild_table(self) -> None:
        entries = TimeEntryService.get_all(self.app.session).all()
        row_data = [entry.to_list() for entry in entries]
        self.table.delete_rows()
        self.table.insert_rows(tb.END, row_data)
        self.table.load_table_data()

    def start_new_entry(self) -> None:
        self.te_form.form_for_new_entry()

    def resume_entry(self, curr_pause_duration: timedelta) -> None:
        self.te_form.te_pause.delete(0, tb.END)
        self.te_form.te_pause.insert(0, str(curr_pause_duration).split(".", 2)[0])

    def stop_entry(self, curr_duration: timedelta) -> None:
        self.te_form.te_end.delete(0, tb.END)
        self.te_form.te_end.insert(0, datetime.now().strftime("%H:%M:%S"))

        self.te_form.te_duration["text"] = str(curr_duration).split(".", 2)[0]
