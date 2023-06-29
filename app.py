#!/usr/bin/python

# Python libraries
from tkinter import Tk, ttk
import configparser
from datetime import datetime
# Custom libraries
from src.model.orm_base import Session, db_engine, Base
from src.controller.db_controller import DBController
from src.model.tracking_session import TrackingSession
from src.components.MainFrame import MainFrame


class App(Tk):
    def __init__(self):
        super().__init__()

        # Load and update configuration data
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.config['User']['last_login_datetime'] = str(datetime.now())
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
        
        # Open a new database connection
        Base.metadata.create_all(db_engine)
        self.session = Session()
        self.db_controller = DBController(self.session)

        # GUI structure
        self.title('Time Journal')
        container = MainFrame(self)


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
