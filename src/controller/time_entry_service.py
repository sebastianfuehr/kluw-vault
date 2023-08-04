from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Sequence

from sqlalchemy import func, select

from ..model.time_entry import TimeEntry

if TYPE_CHECKING:
    from sqlalchemy.engine import ScalarResult
    from sqlalchemy.orm import Session


class TimeEntryService:
    def get_all(db_session: Session) -> ScalarResult:
        stmt = select(TimeEntry)
        results = db_session.execute(stmt)
        return results.scalars()

    def get_all_today(db_session: Session) -> Sequence[TimeEntry]:
        stmt = select(TimeEntry).filter(func.DATE(TimeEntry.start) == date.today())
        results = db_session.execute(stmt)
        return results.scalars().all()

    def merge(db_session: Session, te: TimeEntry) -> None:
        """Inserts or updates a record."""
        print(f"merge with {te.to_list()}")
        db_session.merge(te)
        db_session.commit()
