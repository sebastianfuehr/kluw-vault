#!/usr/bin/python

# Python libraries
import ttkbootstrap as tb
from tkinter.font import nametofont
import configparser
from datetime import datetime
# Custom libraries
from src.model.orm_base import Session, db_engine, Base
from src.model.tracking_session import TrackingSession
from src.components.MainFrame import MainFrame
# Unused imports needed for relationship creation of SQLAlchemy
from src.model.activity import Activity
from src.model.project_tag import ProjectTag
from src.model.rel_project_tag import RelProjectTag
from src.model.project_category import ProjectCategory
from src.model.project_category_goal import ProjectCategoryGoal
# Controller
from src.controller.statistics_controller import StatisticsController
from src.controller.project_category_goal_stats_controller import ProjectCategoryGoalStatsController
from src.controller.file_controller import FileController


class App(tb.Window):
    def __init__(self):
        super().__init__(themename='darkly')

        # Load and update configuration data
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.config['User']['last_login_datetime'] = str(datetime.now())
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

        # Options
        default_font = nametofont('TkDefaultFont')
        default_font.configure(size=16)

        # Open a new database connection
        Base.metadata.create_all(db_engine)
        self.session = Session()
        self.db_engine = db_engine

        self.sc = StatisticsController(self.session)
        self.pcgsc = ProjectCategoryGoalStatsController(self.session)
        self.file_controller = FileController(self)

        # GUI structure
        self.title('Time Journal')
        MainFrame(self)

    def update_statistics_sidebar(self, added_duration):
        self.stats_sidebar.update_total_time(added_duration)
        # self.stats_sidebar.update_goal_progress()


if __name__ == '__main__':
    session_start = datetime.now()

    app = App()
    app.mainloop()

    # Close the database connection and save tracking session data
    session_end = datetime.now()
    session_data = TrackingSession(start=session_start, end=session_end)
    app.session.add(session_data)
    app.session.commit()
    app.session.close()
