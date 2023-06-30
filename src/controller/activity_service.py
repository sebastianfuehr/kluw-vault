from sqlalchemy import select
from ..model.activity import Activity


class ActivityService():

    def get_all(db_session):
        stmt = select(Activity)
        results = db_session.execute(stmt)
        return results.scalars()

    def get_activity_id(db_session, activity_name, project_id):
        stmt = select(Activity).filter_by(name=activity_name)
        result = db_session.execute(stmt).fetchone()[0]
        return result

    def get_activity_name(db_session, activity_id):
        stmt = select(Activity).filter_by(id=activity_id)
        result = db_session.execute(stmt).fetchone()
        return result
