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
from src.model.tag import Tag
from src.model.project_tag import ProjectTag


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

        # GUI structure
        self.title('Time Journal')
        MainFrame(self)


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
