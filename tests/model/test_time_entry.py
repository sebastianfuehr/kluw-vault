import unittest
from datetime import datetime, timedelta
from src.model.time_entry import TimeEntry
# Imports needed solely for sqlalchemy
from src.model.project import Project
from src.model.project_tag import ProjectTag
from src.model.rel_project_tag import RelProjectTag
from src.model.project_category import ProjectCategory
from src.model.activity import Activity


class TestProjectCategoryGoal(unittest.TestCase):
    def setUp(self):
        self.start = datetime(2023, 7, 21, 10, 10, 10)
        self.stop = datetime(2023, 7, 21, 11, 12, 18)
        self.project = Project(id=1, name="Test Project")
        self.activity = Activity(id=0, name="Test Activity")
        self.time_entry = TimeEntry(
            id=260,
            start=self.start,
            stop=self.stop,
            pause=62,
            project_id=self.project.id,
            project_name=self.project.name,
            activity_id=self.activity.id,
            activity_name=self.activity.name
        )

    def test_get_weekday(self):
        self.assertEqual(
            self.time_entry.get_weekday(),
            "Fri"
        )
    
    def test_get_pause_timedelta(self):
        self.assertEqual(
            self.time_entry.get_pause_timedelta(),
            timedelta(seconds=62)
        )

    def test_get_duration_timedelta(self):
        self.assertEqual(
            self.time_entry.get_duration_timedelta(),
            timedelta(seconds=3666)
        )
    
    def test_get_duration_minutes(self):
        self.assertEqual(
            self.time_entry.get_duration_minutes(),
            3666/60
        )

    def test_to_list(self):
        self.assertEqual(
            self.time_entry.to_list(),
            [
                260, # ID
                self.start.date(), # Date
                "Fri", # Weekday
                self.start.time(), # Start time
                self.stop.time(), # End time
                timedelta(seconds=62), # Pause (timedelta)
                timedelta(seconds=3666), # Duration (timedelta)
                self.project.id, # Project ID
                self.project.name, # Project name
                self.activity.id, # Activity ID
                self.activity.name, # Activity name
                True, # Alone
                None, # Tags
                None # Comment
            ]
        )

    def test_from_list(self):
        te_list = [
            260,
            "2023-07-21",
            "Fri",
            "10:10:10",
            "11:12:18",
            "0:01:02",
            "TEST",
            str(self.project.id),
            self.project.name,
            str(self.activity.id),
            self.activity.name,
            True,
            None,
            None
        ]
        te_from_list = TimeEntry.from_list(te_list)
        self.assertEqual(
            self.time_entry,
            te_from_list,
            f"{self.time_entry.to_list()} vs. {te_from_list.to_list()}"
        )