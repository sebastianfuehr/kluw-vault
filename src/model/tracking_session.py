from sqlalchemy import Column, Integer, DateTime
from .orm_base import Base

class TrackingSession(Base):
    __tablename__ = 'tracking_sessions'
    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    end = Column(DateTime)

    def __init__(self, start, end):
        self.start = start
        self.end = end