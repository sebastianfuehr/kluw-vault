from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .orm_base import Base


class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="activities")

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
