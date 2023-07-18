from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from .orm_base import Base


class ProjectTag(Base):
    __tablename__ = "project_tags"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    projects = relationship(
        "Project", secondary="rel_project_tags", back_populates="project_tags"
    )

    def __init__(self, name):
        self.name = name
