from datetime import date, datetime, time, timedelta
from types import NotImplementedType
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.activity import Activity
from src.model.project import Project

from .orm_base import Base


class TimeEntry(Base):
    """A representation of a time entry, spent working on a project of
    some kind.

    Attributes
        __tablename__: The table name inside the database.
        id:
        start:
        stop:
        pause:
        project_id:
        project:
        activity_id:
        activity:
    """

    __tablename__ = "time_entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start: Mapped[datetime] = mapped_column(DateTime)
    stop: Mapped[datetime] = mapped_column(DateTime)
    pause: Mapped[int] = mapped_column(Integer)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship("Project")
    activity_id: Mapped[int] = mapped_column(Integer, ForeignKey("activities.id"))
    activity: Mapped["Activity"] = relationship("Activity")
    tags: Mapped[str] = mapped_column(String)
    alone: Mapped[bool] = mapped_column(Boolean)
    comment: Mapped[str] = mapped_column(Text)

    def __init__(
        self,
        id: Optional[int] = None,
        start: Optional[datetime] = None,
        stop: Optional[datetime] = None,
        pause: float = 0,
        project_id: Optional[int] = None,
        project_name: Optional[str] = None,
        activity_id: Optional[int] = None,
        activity_name: Optional[str] = None,
        alone: bool = True,
        tags: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> None:
        self.id = id
        if start is not None:
            self.start = start
        else:
            self.start = None
        if stop is not None:
            self.stop = stop
        else:
            self.stop = None
        self.pause = int(pause)
        self.project_id = project_id
        # self.project_name = project_name
        self.project = Project(id=self.project_id, name=project_name)
        self.activity_id = activity_id
        # self.activity_name = activity_name
        self.activity = Activity(id=self.activity_id, name=activity_name)
        self.alone = alone
        self.tags = tags
        self.comment = comment

    # GETTER AND SETTER #######################################################

    def get_date(self) -> date:
        return self.start.date()

    def get_weekday_str(self) -> str:
        """Returns the weekday of the date of the time entry in a short
        string format.

        Returns
            weekday: A string in the format "%a", e.g., "We".
        """
        return self.start.strftime("%a")

    def get_start_time(self) -> time:
        return self.start.time()

    def get_end_time(self) -> time:
        return self.stop.time()

    def get_pause_seconds(self) -> float:
        return self.pause

    def get_pause_timedelta(self) -> timedelta:
        return timedelta(seconds=self.pause)

    def get_duration_timedelta(self) -> timedelta:
        duration = timedelta(seconds=0)
        if self.start is not None and self.stop is not None:
            duration = self.stop - self.start - self.get_pause_timedelta()
        return duration

    def get_duration_minutes(self) -> float:
        return self.get_duration_timedelta().total_seconds() / 60

    def get_project_name(self) -> str | None:
        if self.project is not None:
            return self.project.name
        else:
            return None

    def get_activity_name(self) -> str | None:
        if self.activity is None:
            return None
        else:
            return self.activity.name

    # MISC. ###################################################################

    @staticmethod
    def get_column_names() -> List[str]:
        return [
            "db_id",
            "Date",
            "Day",
            "Start",
            "Stop",
            "Pause",
            "Duration",
            "Project ID",
            "Project Name",
            "Activity ID",
            "Activity Name",
            "Alone",
            "Tags",
            "Comment",
        ]

    def to_list(self) -> list:
        return [
            self.id,
            self.get_date(),
            self.get_weekday_str(),
            self.get_start_time(),
            self.get_end_time(),
            self.get_pause_timedelta(),
            self.get_duration_timedelta(),
            self.project_id,
            self.get_project_name(),
            self.activity_id,
            self.get_activity_name(),
            self.alone,
            self.tags,
            self.comment,
        ]

    @staticmethod
    def from_list(time_entry_list: list) -> "TimeEntry":
        """Transforms a list with parameters into a new TimeEntry
        object.

        Args
            time_entry_list: A list which should correspond to the
            output of TimeEntry.to_list().
        """
        start = datetime.strptime(
            f"{time_entry_list[1]} {time_entry_list[3]}", "%Y-%m-%d %H:%M:%S"
        )
        stop = None
        if time_entry_list[3] != "None":
            stop = datetime.strptime(
                f"{time_entry_list[1]} {time_entry_list[4]}",
                "%Y-%m-%d %H:%M:%S",
            )
        pause_datetime = datetime.strptime(time_entry_list[5], "%H:%M:%S")
        pause_duration = timedelta(
            hours=pause_datetime.hour,
            minutes=pause_datetime.minute,
            seconds=pause_datetime.second,
        )
        if time_entry_list[13] == "":
            comment = None
        else:
            comment = time_entry_list[13]
        new_entry = TimeEntry(
            id=time_entry_list[0],
            start=start,
            stop=stop,
            pause=pause_duration.total_seconds(),
            project_id=int(time_entry_list[7]),
            project_name=time_entry_list[8],
            activity_id=int(time_entry_list[9]),
            activity_name=time_entry_list[10],
            alone=time_entry_list[11],
            tags=time_entry_list[12],
            comment=comment,
        )
        return new_entry

    def __eq__(self, other: object) -> bool | NotImplementedType:
        if not isinstance(other, TimeEntry):
            return NotImplemented
        return (
            self.id == other.id
            and self.start == other.start
            and self.stop == other.stop
            and self.pause == other.pause
            and self.project == other.project
            and self.activity == other.activity
            and self.alone == other.alone
            and self.tags == other.tags
            and self.comment == other.comment
        )
