from sqlalchemy import select, func
from ..model.time_entry import TimeEntry
from datetime import date


class StatisticsController():
    def __init__(self, db_session):
        self.db_session = db_session

    def total_time_today(self):
        """Returns the total worktime of today in seconds.
        """
        stmt = select(TimeEntry)\
            .filter(func.DATE(TimeEntry.start) == date.today())
        results = self.db_session.execute(stmt).scalars().all()

        sec_total = 0
        for entry in results:
            sec_total += entry.get_duration_timedelta().total_seconds()

        return sec_total
