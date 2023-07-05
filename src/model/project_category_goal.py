from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .orm_base import Base


class ProjectCategoryGoal(Base):
    __tablename__ = 'project_category_goals'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    project_category_id = Column(Integer, ForeignKey('project_categories.id'))
    project_category = relationship('ProjectCategory')
    min_monday = Column(Integer)
    min_tuesday = Column(Integer)
    min_wednesday = Column(Integer)
    min_thursday = Column(Integer)
    min_friday = Column(Integer)
    min_saturday = Column(Integer)
    min_sunday = Column(Integer)
    active = Column(Boolean)

    def to_list(self):
        return [
            self.id,
            self.project_category_id,
            self.description
        ]

    def get_weekday_minute_goal(self, weekday):
        match weekday:
            case 0: return self.min_monday
            case 1: return self.min_tuesday
            case 2: return self.min_wednesday
            case 3: return self.min_thursday
            case 4: return self.min_friday
            case 5: return self.goal.min_saturday
            case 6: return self.min_sunday
