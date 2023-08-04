from datetime import datetime, timedelta

import pytest

from src.model.activity import Activity

# Imports needed solely for sqlalchemy
from src.model.project import Project
from src.model.project_category import ProjectCategory  # noqa: F401
from src.model.project_tag import ProjectTag  # noqa: F401
from src.model.rel_project_tag import RelProjectTag  # noqa: F401
from src.model.time_entry import TimeEntry


@pytest.fixture
def default_time_entry():
    start = datetime(2023, 7, 21, 10, 10, 10)
    stop = datetime(2023, 7, 21, 11, 12, 18)
    project = Project(id=1, name="Test Project")
    activity = Activity(id=0, name="Test Activity")
    return TimeEntry(
        id=260,
        start=start,
        stop=stop,
        pause=62,
        project_id=project.id,
        project_name=project.name,
        activity_id=activity.id,
        activity_name=activity.name,
    )


def test_get_weekday(default_time_entry):
    assert default_time_entry.get_weekday_str() == "Fr"


def test_get_pause_timedelta(default_time_entry):
    assert default_time_entry.get_pause_timedelta() == timedelta(seconds=62)


def test_get_duration_timedelta(default_time_entry):
    assert default_time_entry.get_duration_timedelta() == timedelta(seconds=3666)


def test_get_duration_minutes(default_time_entry):
    assert default_time_entry.get_duration_minutes() == 3666 / 60


@pytest.mark.skip
def test_to_list(default_time_entry):
    assert default_time_entry.to_list() == [
        260,  # ID
        default_time_entry.start.date(),  # Date
        "Fr",  # Weekday
        default_time_entry.start.time(),  # Start time
        default_time_entry.stop.time(),  # End time
        timedelta(seconds=62),  # Pause (timedelta)
        timedelta(seconds=3666),  # Duration (timedelta)
        default_time_entry.project.id,  # Project ID
        default_time_entry.project.name,  # Project name
        default_time_entry.activity.id,  # Activity ID
        default_time_entry.activity.name,  # Activity name
        True,  # Alone
        None,  # Tags
        None,  # Comment
    ]


@pytest.mark.skip
def test_from_list(default_time_entry):
    te_list = [
        260,
        "2023-07-21",
        "Fri",
        "10:10:10",
        "11:12:18",
        "0:01:02",
        "TEST",
        str(project.id),
        project.name,
        str(activity.id),
        activity.name,
        True,
        None,
        None,
    ]
    te_from_list = TimeEntry.from_list(te_list)
    assert default_time_entry == te_from_list
