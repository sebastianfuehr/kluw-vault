from sqlalchemy import select
from ..model.project import Project


class ProjectService():

    def get_all(db_session):
        stmt = select(Project)
        results = db_session.execute(stmt)
        return results.scalars()

    def get_project_by_name(db_session, project_name):
        stmt = select(Project).filter_by(name=project_name)
        result = db_session.execute(stmt).fetchone()[0]
        return result
