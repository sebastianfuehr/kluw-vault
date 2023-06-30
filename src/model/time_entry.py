from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from .orm_base import Base


class TimeEntry(Base):
    __tablename__ = 'time_entries'
    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    stop = Column(DateTime)
    pause = Column(Integer)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project')

    def __init__(self,
                 id=None,
                 start=None,
                 stop=None,
                 pause=0):
        """
        Parameters
        ----------
        pause: Integer
            A pause in seconds.
        """
        self.id = id
        if start is not None:
            self.start = start
        else:
            self.start = None
        if stop is not None:
            self.stop = stop
        else:
            self.stop = None
        self.pause = int(pause)

    # GETTER AND SETTER #######################################################

    def get_date(self):
        if self.start is None:
            return None
        else:
            return self.start.date()

    def get_weekday(self):
        if self.start is None:
            return None
        else:
            return self.start.strftime('%a')

    def get_start_time(self):
        if self.start is None:
            return None
        else:
            return self.start.time()

    def get_end_time(self):
        if self.stop is None:
            return None
        else:
            return self.stop.time()

    def get_pause_seconds(self):
        return self.pause

    def get_pause_timedelta(self):
        if self.pause is not None:
            return timedelta(seconds=self.pause)
        else:
            return None

    def get_duration_timedelta(self):
        duration = timedelta(seconds=0)
        if self.start is not None and self.stop is not None:
            duration = self.stop - self.start + self.get_pause_timedelta()
        return duration

    # MISC. ###################################################################

    def to_list(self):
        return [
            self.id,
            self.get_date(),
            self.get_weekday(),
            self.get_start_time(),
            self.get_end_time(),
            self.get_pause_seconds(),
            self.get_duration_timedelta()
        ]

    def from_list(time_entry_list):
        start = datetime.strptime(
            f'{time_entry_list[1]} {time_entry_list[3]}',
            '%Y-%m-%d %H:%M:%S')
        stop = None
        if time_entry_list[3] != 'None':
            stop = datetime.strptime(
                f'{time_entry_list[1]} {time_entry_list[3]}',
                '%Y-%m-%d %H:%M:%S'
            )
        new_entry = TimeEntry(
            id=time_entry_list[0],
            start=start,
            stop=stop,
            pause=time_entry_list[5]
        )
        return new_entry
