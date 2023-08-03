from sqlalchemy import delete, select

from ..model.project_category import ProjectCategory


class ProjectCategoryService:
    @staticmethod
    def get_all(db_session):
        stmt = select(ProjectCategory)
        results = db_session.execute(stmt)
        return results.scalars()

    @staticmethod
    def get_by_id(db_session, category_id):
        stmt = select(ProjectCategory).filter_by(id=category_id)
        result = db_session.execute(stmt).fetchone()[0]
        return result

    @staticmethod
    def get_category_by_name(db_session, category_name):
        stmt = select(ProjectCategory).filter_by(name=category_name)
        result = db_session.execute(stmt).fetchone()[0]
        return result

    @staticmethod
    def merge(db_session, project_category: ProjectCategory):
        """Insert or update a record."""
        db_session.merge(project_category)
        db_session.commit()

    @staticmethod
    def delete(db_session, category_id) -> int:
        """Deletes the entry with the specified ID. Returns the number
        of entries affected by the operation. Should be 1.
        """
        stmt = delete(ProjectCategory).where(ProjectCategory.id == category_id)
        result = db_session.execute(stmt)
        return result.rowcount
