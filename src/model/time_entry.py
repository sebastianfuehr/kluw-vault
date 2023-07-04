from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean, Text, String
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
    activity_id = Column(Integer, ForeignKey('activities.id'))
    activity = relationship('Activity')
    tags = Column(String)
    alone = Column(Boolean)
    comment = Column(Text)

    def __init__(self,
                 id=None,
                 start=None,
                 stop=None,
                 pause=0,
                 project_id=None,
                 project_name=None,
                 activity_id=None,
                 activity_name=None,
                 alone=True,
                 tags=None,
                 comment=None):
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
        self.project_id = project_id
        self.project_name = project_name
        self.activity_id = activity_id
        self.activity_name = activity_name
        self.alone = alone
        self.tags = tags
        self.comment = comment

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
            duration = self.stop - self.start - self.get_pause_timedelta()
        return duration

    def get_duration_minutes(self):
        return self.get_duration_timedelta().total_seconds() / 60

    def get_project_name(self):
        if self.project is not None:
            return self.project.name
        elif self.project_name is not None:
            return self.project_name
        else:
            return None

    def get_activity_name(self):
        if self.activity is not None:
            return self.activity.name
        elif self.activity_name is not None:
            return self.activity_name
        else:
            return None

    # MISC. ###################################################################

    def get_column_names():
        return [
            'db_id',
            'Date',
            'Day',
            'Start',
            'Stop',
            'Pause',
            'Duration',
            'Project ID',
            'Project Name',
            'Activity ID',
            'Activity Name',
            'Alone',
            'Tags',
            'Comment'
        ]

    def to_list(self):
        return [
            self.id,
            self.get_date(),
            self.get_weekday(),
            self.get_start_time(),
            self.get_end_time(),
            self.get_pause_timedelta(),
            self.get_duration_timedelta(),
            self.project_id,
            self.get_project_name(),
            self.activity_id,
            self.get_activity_name(),
            self.alone,
            self.tags,
            self.comment
        ]

    def from_list(time_entry_list):
        start = datetime.strptime(
            f'{time_entry_list[1]} {time_entry_list[3]}',
            '%Y-%m-%d %H:%M:%S')
        stop = None
        if time_entry_list[3] != 'None':
            stop = datetime.strptime(
                f'{time_entry_list[1]} {time_entry_list[4]}',
                '%Y-%m-%d %H:%M:%S'
            )
        pause_datetime = datetime.strptime(time_entry_list[5], '%H:%M:%S')
        pause_duration = timedelta(hours=pause_datetime.hour,
                                   minutes=pause_datetime.minute,
                                   seconds=pause_datetime.second)
        new_entry = TimeEntry(
            id=time_entry_list[0],
            start=start,
            stop=stop,
            pause=pause_duration.total_seconds(),
            project_id=time_entry_list[7],
            project_name=time_entry_list[8],
            activity_id=time_entry_list[9],
            activity_name=time_entry_list[10],
            alone=time_entry_list[11],
            tags=time_entry_list[12],
            comment=time_entry_list[13]
        )
        return new_entry
