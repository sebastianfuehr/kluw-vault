from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from .orm_base import Base


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    projects = relationship('Project',
                            secondary='project_tags',
                            back_populates='tags')

    def __init__(self, name):
        self.name = name
