from sqlalchemy import Column, Integer, String
from .orm_base import Base


class ProjectCategory(Base):
    __tablename__ = 'project_categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
