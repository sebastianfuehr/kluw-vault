from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from .orm_base import Base


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tags = relationship('Tag',
                        secondary='project_tags',
                        back_populates='projects')

    def __init__(self,
                 id=None,
                 name=None):
        self.id = id
        self.name = name

    def to_string(self):
        return f'id: {self.id}, name: {self.name}'
