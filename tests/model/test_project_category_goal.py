import unittest

# Imports with noqa: F401 only needed for SQLAlchemy
from src.model.project_category import ProjectCategory  # noqa: F401
from src.model.project_category_goal import ProjectCategoryGoal


class TestProjectCategoryGoal(unittest.TestCase):
    def setUp(self):
        self.goal_list = [50, 200, 100, 100, 100, 0, 25]
        self.project_category_goal = ProjectCategoryGoal(
            id=None,
            min_monday=self.goal_list[0],
            min_tuesday=self.goal_list[1],
            min_wednesday=self.goal_list[2],
            min_thursday=self.goal_list[3],
            min_friday=self.goal_list[4],
            min_saturday=self.goal_list[5],
            min_sunday=self.goal_list[6],
        )

    def test_to_list(self):
        self.assertEqual(
            self.project_category_goal.to_list(),
            [None, None, None],  # ID  # Category ID  # Description
        )

    def test_get_goal_list(self):
        self.assertEqual(self.project_category_goal.get_goal_list(), self.goal_list)
