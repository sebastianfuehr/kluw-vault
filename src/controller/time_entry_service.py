from sqlalchemy import select
from ..model.time_entry import TimeEntry


class TimeEntryService():

    def get_all(db_session):
        stmt = select(TimeEntry)
        results = db_session.execute(stmt)
        return results.scalars()

    def merge(db_session, te: TimeEntry):
        """Inserts or updates a record.
        """
        output = db_session.merge(te)
        db_session.commit()
        print(f'merge outpu: {output.to_list()}')
