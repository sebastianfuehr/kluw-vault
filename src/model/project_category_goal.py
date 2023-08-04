from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .orm_base import Base

if TYPE_CHECKING:
    from src.model.project_category import ProjectCategory


class ProjectCategoryGoal(Base):
    __tablename__ = "project_category_goals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String)
    project_category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("project_categories.id")
    )
    project_category: Mapped[ProjectCategory] = relationship("ProjectCategory")
    min_monday = mapped_column(Integer)
    min_tuesday = mapped_column(Integer)
    min_wednesday = mapped_column(Integer)
    min_thursday = mapped_column(Integer)
    min_friday = mapped_column(Integer)
    min_saturday = mapped_column(Integer)
    min_sunday = mapped_column(Integer)
    active = mapped_column(Boolean)

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
    ) -> None:
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

    def get_weekday_minute_goal(self, weekday: int) -> int:
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
