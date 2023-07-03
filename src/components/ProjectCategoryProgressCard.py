import ttkbootstrap as tb


class ProjectCategoryProgressCard(tb.Frame):
    def __init__(self, parent, app, goal):
        super().__init__(parent)
        self.parent = parent
        self.config = parent.config
        self.app = app
        self.goal = goal
        self.goal_progress = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.__build_gui_components()

    def __build_gui_components(self):
        lbl_goal = tb.Label(
            self,
            text=self.goal.name, justify='left'
        )
        lbl_goal.grid(row=0, column=0, sticky='w')
        self.lbl_goal_progress = tb.Label(
            self,
            text=f'{self.goal_progress}/{self.goal.goal_minutes}m',
            justify='right'
        )
        self.lbl_goal_progress.grid(row=0, column=1, sticky='e')
        self.fg_goal_progress = tb.Floodgauge(
            self,
            maximum=self.goal.goal_minutes
        )
        self.fg_goal_progress.grid(row=1, column=0, columnspan=2, sticky='ew')

    def update_progress(self, progress_value: int):
        if progress_value > self.goal.goal_minutes:
            new_progress_value = self.goal.goal_minutes
            self.fg_goal_progress.configure(bootstyle='success')
        else:
            new_progress_value = progress_value
        progress_str = f'{new_progress_value}/{self.goal.goal_minutes}m'
        self.lbl_goal_progress['text'] = progress_str
        self.fg_goal_progress.configure(value=new_progress_value)
