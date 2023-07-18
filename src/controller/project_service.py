from sqlalchemy import select, delete
from ..model.project import Project


class ProjectService:
    @staticmethod
    def get_all(db_session):
        stmt = select(Project)
        results = db_session.execute(stmt)
        return results.scalars()

    @staticmethod
    def get_project_by_name(db_session, project_name):
        stmt = select(Project).filter_by(name=project_name)
        result = db_session.execute(stmt).fetchone()[0]
        return result

    @staticmethod
    def get_by_category_id(db_session, category_id):
        stmt = select(Project).filter_by(project_category_id=category_id)
        result = db_session.execute(stmt)
        return result.scalars()

    @staticmethod
    def get_by_id(db_session, project_id):
        stmt = select(Project).filter_by(id=project_id)
        result = db_session.execute(stmt).fetchone()[0]
        return result

    @staticmethod
    def merge(db_session, project: Project):
        """Insert or update a record."""
        db_session.merge(project)
        db_session.commit()

    def delete(db_session, project_id) -> int:
        """Deletes the entry with the specified ID. Returns the number
        of entries affected by the operation. Should be 1.
        """
        stmt = delete(Project).where(Project.id == project_id)
        result = db_session.execute(stmt)
        return result.rowcount
