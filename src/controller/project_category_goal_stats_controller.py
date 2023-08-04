from datetime import date
from typing import TYPE_CHECKING, Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..model.project import Project
from ..model.project_category import ProjectCategory
from ..model.project_category_goal import ProjectCategoryGoal
from ..model.time_entry import TimeEntry

if TYPE_CHECKING:
    pass


class ProjectCategoryGoalStatsController:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def get_active_goals(self) -> Sequence[ProjectCategoryGoal]:
        stmt = select(ProjectCategoryGoal).filter(ProjectCategoryGoal.active)
        results = self.db_session.execute(stmt).scalars().all()
        return results

    def get_time_entries_per_category(self) -> Sequence[TimeEntry]:
        stmt = (
            select(ProjectCategory.id, TimeEntry)
            .filter(func.DATE(TimeEntry.start) == date.today())
            .join(Project, TimeEntry.project_id == Project.id)
            .join(
                ProjectCategory,
                Project.project_category_id == ProjectCategory.id,
            )
        )
        results = self.db_session.execute(stmt).all()
        return results
