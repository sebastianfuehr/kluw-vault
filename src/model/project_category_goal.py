from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .orm_base import Base


class ProjectCategoryGoal(Base):
    __tablename__ = 'project_category_goals'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    weekday = Column(Integer)
    description = Column(String)
    goal_minutes = Column(Integer)
    project_category_id = Column(Integer, ForeignKey('project_categories.id'))
    project_category = relationship('ProjectCategory')

    def to_list(self):
        return [
            self.id,
            self.name,
            self.weekday,
            self.description,
            self.goal_minutes,
            self.project_category_id
        ]
