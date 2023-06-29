from sqlalchemy import select
from ..model.tracking_session import TrackingSession

class DBController():
    def __init__(self, db_session):
        self.db_session = db_session


    def get_all(self):
        stmt = select(TrackingSession)
        result = self.db_session.execute(stmt)
        for res in result.scalars():
            print(f"{res.start}")