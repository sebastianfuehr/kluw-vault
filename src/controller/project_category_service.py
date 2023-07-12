from sqlalchemy import select
from ..model.project_category import ProjectCategory


class ProjectCategoryService():
    @staticmethod
    def get_all(db_session):
        stmt = select(ProjectCategory)
        results = db_session.execute(stmt)
        return results.scalars()