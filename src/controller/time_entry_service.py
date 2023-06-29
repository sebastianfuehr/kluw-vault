from sqlalchemy import select
from ..model.time_entry import TimeEntry

class TimeEntryService():

    def get_all(db_session):
        stmt = select(TimeEntry)
        results = db_session.execute(stmt)
        return results.scalars()