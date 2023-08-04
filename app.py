#!/usr/bin/python
from datetime import datetime
from tkinter.font import nametofont

import ttkbootstrap as tb

from config.definitions import Definitions
from src.components.main_frame import MainFrame
from src.controller.data_controller import DataController
from src.controller.file_controller import FileController
from src.controller.project_category_goal_stats_controller import (
    ProjectCategoryGoalStatsController,
)
from src.controller.statistics_controller import StatisticsController

# Unused noqa: F401 imports are needed for the relationship creation of
# SQLAlchemy
from src.model.activity import Activity  # noqa: F401
from src.model.orm_base import Base, DBConnection  # Session, db_engine, Base
from src.model.project_category import ProjectCategory  # noqa: F401
from src.model.project_category_goal import ProjectCategoryGoal  # noqa: F401
from src.model.project_tag import ProjectTag  # noqa: F401
from src.model.rel_project_tag import RelProjectTag  # noqa: F401
from src.model.tracking_session import TrackingSession


class App(tb.Window):  # type: ignore
    def __init__(self, db_connection: DBConnection) -> None:
        # Load config data
        self.definitions: Definitions = Definitions()
        self.settings = self.definitions.load_config()
        theme = self.settings["appearance"]["theme"]
        super().__init__(title="Time Journal", themename=theme, minsize=(1080, 800))

        # Options
        default_font = nametofont("TkDefaultFont")
        default_font.configure(size=16)
        self.option_add("*TCombobox*Listbox*Font", (None, 16))

        # Open a new database connection
        Base.metadata.create_all(db_connection.db_engine)
        self.session = db_connection.Session()
        self.db_engine = db_connection.db_engine

        self.sc = StatisticsController(self.session)
        self.dc = DataController(self.session)
        self.pcgsc = ProjectCategoryGoalStatsController(self.session)
        self.file_controller = FileController(self)

        # GUI structure
        self.main_frame = MainFrame(self)

    def start(self) -> None:
        self.session_start = datetime.now()
        self.mainloop()

    def stop(self) -> None:
        """Save the session data into the database and close the database connection."""
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
