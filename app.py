#!/usr/bin/python
# Python libraries
import ttkbootstrap as tb
from tkinter.font import nametofont
from datetime import datetime

# Custom libraries
from src.model.orm_base import Session, db_engine, Base
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
from src.controller.statistics_controller import StatisticsController
from src.controller.project_category_goal_stats_controller import ProjectCategoryGoalStatsController
from src.controller.file_controller import FileController


class App(tb.Window):
    def __init__(self):
        super().__init__(
            title='Time Journal',
            themename='darkly',
            minsize=(1080, 800)
        )

        # Load and update configuration data
        self.settings = SettingsController.load_or_create_config_file()

        # Options
        default_font = nametofont('TkDefaultFont')
        default_font.configure(size=16)
        self.option_add("*TCombobox*Listbox*Font", (None, 16))

        # Open a new database connection
        Base.metadata.create_all(db_engine)
        self.session = Session()
        self.db_engine = db_engine

        self.sc = StatisticsController(self.session)
        self.pcgsc = ProjectCategoryGoalStatsController(self.session)
        self.file_controller = FileController(self)

        # GUI structure
        MainFrame(self)

        session_start = datetime.now()
        self.mainloop()

        # Close the database connection and save tracking session data
        session_end = datetime.now()
        session_data = TrackingSession(start=session_start, end=session_end)
        self.session.add(session_data)
        self.session.commit()
        self.session.close()


if __name__ == '__main__':
    app = App()
