#!/usr/bin/python
# Python libraries
import logging
import os
import ttkbootstrap as tb
from tkinter.font import nametofont
from datetime import datetime

# Custom libraries
from src.model.orm_base import DBConnection, Base # Session, db_engine, Base
from src.model.tracking_session import TrackingSession
from src.components.main_frame import MainFrame

# Unused imports needed for relationship creation of SQLAlchemy
from src.model.activity import Activity
from src.model.project_tag import ProjectTag
from src.model.rel_project_tag import RelProjectTag
from src.model.project_category import ProjectCategory
from src.model.project_category_goal import ProjectCategoryGoal

# Controller
from src.controller.settings_controller import SettingsController
from src.controller.data_controller import DataController
from src.controller.statistics_controller import StatisticsController
from src.controller.project_category_goal_stats_controller import (
    ProjectCategoryGoalStatsController,
)
from src.controller.file_controller import FileController
from config.definitions import Definitions


class App(tb.Window):
    def __init__(self, db_connection):
        # Load config data
        self.definitions = Definitions()
        self.settings = self.definitions.load_config()
        theme = self.settings["appearance"]["theme"]
        super().__init__(
            title="Time Journal", themename=theme, minsize=(1080, 800)
        )

        # Options
        default_font = nametofont("TkDefaultFont")
        default_font.configure(size=16)
        self.option_add("*TCombobox*Listbox*Font", (None, 16))

        # Open a new database connection
        #self.db_conn = DBConnection("/time-journal.db")
        Base.metadata.create_all(db_connection.db_engine)
        self.session = db_connection.Session()
        self.db_engine = db_connection.db_engine

        self.sc = StatisticsController(self.session)
        self.dc = DataController(self.session)
        self.pcgsc = ProjectCategoryGoalStatsController(self.session)
        self.file_controller = FileController(self)

        # GUI structure
        self.main_frame = MainFrame(self)

    def start(self):
        self.session_start = datetime.now()
        self.mainloop()

    def stop(self):
        """Save the session data into the database and close the database connection.
        """
        session_end = datetime.now()
        session_data = TrackingSession(start=self.session_start, end=session_end)
        self.session.add(session_data)
        self.session.commit()
        self.session.close()


if __name__ == "__main__":
    db_connection = DBConnection("/time-journal.db")
    app = App(db_connection)
    app.start()
    app.stop()
