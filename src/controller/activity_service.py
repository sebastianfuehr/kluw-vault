from sqlalchemy import select # pylint: disable=import-error
from ..model.activity import Activity


class ActivityService():

    @staticmethod
    def get_all(db_session):
        stmt = select(Activity)
        results = db_session.execute(stmt)
        return results.scalars()

    @staticmethod
    def get_activity_id(db_session, activity_name, project_id):
        stmt = select(Activity).filter_by(name=activity_name)
        result = db_session.execute(stmt).fetchone()[0]
        return result

    @staticmethod
    def get_activity_name(db_session, activity_id):
        stmt = select(Activity).filter_by(id=activity_id)
        result = db_session.execute(stmt).fetchone()
        return result
