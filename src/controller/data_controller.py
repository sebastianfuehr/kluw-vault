import pandas as pd
from .. model.time_entry import TimeEntry
from .. controller.time_entry_service import TimeEntryService


class DataController:
    """A central entity that manages the data of the application."""
    def __init__(self, db_session):
        self.db_session = db_session

        # Various data frames with specific capabilities
        self.time_entry_df = None

        self.refresh_all_data()

    def refresh_all_data(self):
        """Refresh the data of the controller."""
        self.refresh_time_entry_df()

    def refresh_time_entry_df(self):
        time_entry_objects = TimeEntryService.get_all(self.db_session).all()
        time_entries= [entry.to_list() for entry in time_entry_objects]
        self.time_entry_df = pd.DataFrame(
            time_entries, columns=TimeEntry.get_column_names()
        )
        if len(self.time_entry_df) == 0:
            return
        # Pre-processing
        self.time_entry_df["Date"] = pd.to_datetime(
            self.time_entry_df["Date"], errors="coerce"
        )
