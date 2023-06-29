from sqlalchemy import Column, String, Integer, DateTime
from .orm_base import Base

class TimeEntry(Base):
    __tablename__ = 'time_entries'
    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    stop = Column(DateTime)
    pause = Column(Integer)

    def __init__(self, start, stop=None, pause=0):
        self.start = start
        self.stop = stop
        self.pause = pause
    
    def get_start_time(self):
        if self.start != None:
            return self.start.time()
        else:
            return None
    
    def get_stop_time(self):
        if self.stop != None:
            return self.stop.time()
        else:
            return None
    
    def get_duration(self):
        duration = 0
        if self.start != None and self.stop != None:
            duration = self.start - self.stop - self.pause
        return duration
    
    def get_list(self):
        return [
            self.start.date(),
            self.start.strftime('%a'),
            self.get_start_time(),
            self.get_stop_time(),
            self.pause,
            self.get_duration()
        ]