from sqlalchemy import select
from ..model.project import Project


class ProjectService():
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
    def get_by_id(db_session, project_id):
        stmt = select(Project).filter_by(id=project_id)
        result = db_session.execute(stmt).fetchone()[0]
        return result
    
    @staticmethod
    def merge(db_session, project: Project):
        """Insert or update a record.
        """
        db_session.merge(project)
        db_session.commit()
