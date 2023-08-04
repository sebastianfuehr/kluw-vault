from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.engine import Row, ScalarResult
from sqlalchemy.orm import Session

from ..model.project_category_goal import ProjectCategoryGoal


class ProjectCategoryGoalService:
    @staticmethod
    def get_by_id(db_session: Session, goal_id: int) -> Row:
        stmt = select(ProjectCategoryGoal).filter_by(id=goal_id)
        result = db_session.execute(stmt).fetchone()[0]
        return result

    @staticmethod
    def get_by_category_id(db_session: Session, category_id: int) -> ScalarResult:
        stmt = select(ProjectCategoryGoal).filter_by(project_category_id=category_id)
        result = db_session.execute(stmt)
        return result.scalars()

    @staticmethod
    def merge(db_session: Session, project_category_goal: ProjectCategoryGoal) -> None:
        """Insert or update a record."""
        db_session.merge(project_category_goal)
        db_session.commit()
