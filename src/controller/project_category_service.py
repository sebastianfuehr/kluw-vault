from sqlalchemy import select
from ..model.project_category import ProjectCategory


class ProjectCategoryService():
    @staticmethod
    def get_all(db_session):
        stmt = select(ProjectCategory)
        results = db_session.execute(stmt)
        return results.scalars()

    @staticmethod
    def get_category_by_name(db_session, category_name):
        stmt = select(ProjectCategory).filter_by(name=category_name)
        result = db_session.execute(stmt).fetchone()[0]
        return result
