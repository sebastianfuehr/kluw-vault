from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .orm_base import Base


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    project_category_id = Column(Integer, ForeignKey('project_categories.id'))
    project_category = relationship('ProjectCategory')
    project_tags = relationship('ProjectTag',
                                secondary='rel_project_tags',
                                back_populates='projects')
    activities = relationship('Activity', back_populates='project')

    def __init__(self,
                 id=None,
                 name=None):
        self.id = id
        self.name = name

    @staticmethod
    def get_column_names():
        return [
            'id',
            'Name',
            'Description',
            'Project Category ID',
            'Project Tags'
        ]

    def to_string(self):
        return f'id: {self.id}, name: {self.name}'
