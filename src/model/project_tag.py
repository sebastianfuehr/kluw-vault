from sqlalchemy import Column, Integer, ForeignKey
from .orm_base import Base


class ProjectTag(Base):
    __tablename__ = 'project_tags'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

    def __init__(self):
        print('Test')
