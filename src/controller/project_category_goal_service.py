from sqlalchemy import select, delete
from ..model.project_category_goal import ProjectCategoryGoal


class ProjectCategoryGoalService():

    @staticmethod
    def get_by_id(db_session, goal_id):
        stmt = select(ProjectCategoryGoal).filter_by(id=goal_id)
        result = db_session.execute(stmt).fetchone()[0]
        return result

    @staticmethod
    def get_by_category_id(db_session, category_id):
        stmt = select(ProjectCategoryGoal).filter_by(project_category_id=category_id)
        result = db_session.execute(stmt)
        return result.scalars()

    @staticmethod
    def merge(db_session, project_category_goal: ProjectCategoryGoal):
        """Insert or update a record.
        """
        db_session.merge(project_category_goal)
        db_session.commit()