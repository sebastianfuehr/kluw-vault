import ttkbootstrap as tb

from ..controller.project_category_goal_stats_controller import ProjectCategoryGoalStatsController
from ..model.project_category_goal import ProjectCategoryGoal


class CategoryGoalsList(tb.Frame):
    def __init__(self, parent, app):
        super().__init__(master=parent)
        self.app = app
        self.goals_controller = ProjectCategoryGoalStatsController(self.app.session)

        test = tb.Label(self, text='Test')
        test.pack()

        res = self.goals_controller.get_active_goals()
        print(f'CategoryGoalsList: {res}')
