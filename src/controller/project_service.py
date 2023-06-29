from sqlalchemy import select
from ..model.project import Project

class ProjectService():

    def get_all(db_session):
        stmt = select(Project)
        results = db_session.execute(stmt)
        return results.scalars()