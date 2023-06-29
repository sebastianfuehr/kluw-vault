from tkinter import ttk
import tksheet
# Custom libraries
from ..controller.time_entry_service import TimeEntryService

class TimeEntriesList(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app

        # Table headers
        headers = [
            'Date',
            'Day',
            'Start',
            'Stop',
            'Pause',
            'Duration'
        ]

        entries = TimeEntryService.get_all(self.app.session).all()
        entries_lists = [entry.get_list() for entry in entries]

        sheet = tksheet.Sheet(self, header=headers)
        sheet.pack(fill="both")
        sheet.set_sheet_data(entries_lists)
        sheet.enable_bindings(("single_select",
                               "row_select",
                               "arrowkeys",
                               "column_width_resize",
                               "row_height_resize",
                               "copy",
                               "edit_cell"))
        sheet.readonly_columns(columns=[1,5], readonly=True)
        sheet.align_columns(columns=[3,4,5,], align="e", align_header=False)
        #sheet.format_column(3, formatter_options=)

        """
        # Create table skeleton
        entry_columns = [
            'Date',
            'Day',
            'Start',
            'Stop',
            'Pause',
            'Duration'
        ]
        col_nbr = 0
        for column in entry_columns:
            lbl_header = ttk.Label(self, text=f'{column}')
            lbl_header.grid(row=0, column=col_nbr)
            col_nbr += 1

        # Add entries
        entries = TimeEntryService.get_all(self.app.session)
        row_nbr = 1
        for entry in entries:
            lbl_date = ttk.Label(self, text=f'{entry.start.date()}')
            lbl_date.grid(row=row_nbr, column=0)

            lbl_day = ttk.Label(self, text=f"{entry.start.strftime('%a')}")
            lbl_day.grid(row=row_nbr, column=1)

            lbl_start = ttk.Label(self, text=f'{entry.start}')
            lbl_start.grid(row=row_nbr, column=2)

            lbl_stop = ttk.Label(self, text=f'{entry.stop}')
            lbl_stop.grid(row=row_nbr, column=3)

            lbl_pause = ttk.Label(self, text=f'{entry.pause}')
            lbl_pause.grid(row=row_nbr, column=4)

            duration = 0
            if entry.start != None and entry.stop != None:
                duration = entry.start - entry.stop
            lbl_duration = ttk.Label(self, text=f'{duration}')
            lbl_duration.grid(row=row_nbr, column=5)

            row_nbr += 1
        """