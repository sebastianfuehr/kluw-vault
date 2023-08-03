from datetime import date

from sqlalchemy import func, select

from ..model.project import Project
from ..model.project_category import ProjectCategory
from ..model.project_category_goal import ProjectCategoryGoal
from ..model.time_entry import TimeEntry


class ProjectCategoryGoalStatsController:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_active_goals(self):
        stmt = select(ProjectCategoryGoal).filter(ProjectCategoryGoal.active)
        results = self.db_session.execute(stmt).scalars().all()
        return results

    def get_time_entries_per_category(self):
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
