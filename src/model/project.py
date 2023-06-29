from sqlalchemy import Column, String, Integer, DateTime
from .orm_base import Base

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name