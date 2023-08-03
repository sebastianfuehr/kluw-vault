from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .orm_base import Base


class ProjectCategoryGoal(Base):
    __tablename__ = "project_category_goals"
    id = Column(Integer, primary_key=True)
    description = Column(String)
    project_category_id = Column(Integer, ForeignKey("project_categories.id"))
    project_category = relationship("ProjectCategory")
    min_monday = Column(Integer)
    min_tuesday = Column(Integer)
    min_wednesday = Column(Integer)
    min_thursday = Column(Integer)
    min_friday = Column(Integer)
    min_saturday = Column(Integer)
    min_sunday = Column(Integer)
    active = Column(Boolean)

    def __init__(
        self,
        id: int,
        min_monday=0,
        min_tuesday=0,
        min_wednesday=0,
        min_thursday=0,
        min_friday=0,
        min_saturday=0,
        min_sunday=0,
        active=True,
    ):
        self.id = id
        self.min_monday = min_monday
        self.min_tuesday = min_tuesday
        self.min_wednesday = min_wednesday
        self.min_thursday = min_thursday
        self.min_friday = min_friday
        self.min_saturday = min_saturday
        self.min_sunday = min_sunday
        self.active = active

    def to_list(self):
        return [self.id, self.project_category_id, self.description]

    def get_goal_list(self) -> list:
        """Returns the goal values for all weekdays as a list like
        [min_monday, ..., min_sunday]
        """
        return [
            self.min_monday,
            self.min_tuesday,
            self.min_wednesday,
            self.min_thursday,
            self.min_friday,
            self.min_saturday,
            self.min_sunday,
        ]

    def get_weekday_minute_goal(self, weekday):
        """Returns the minute goal for any given weekday."""
        match weekday:
            case 0:
                return self.min_monday
            case 1:
                return self.min_tuesday
            case 2:
                return self.min_wednesday
            case 3:
                return self.min_thursday
            case 4:
                return self.min_friday
            case 5:
                return self.min_saturday
            case 6:
                return self.min_sunday
