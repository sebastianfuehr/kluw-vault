import ttkbootstrap as tb

# GUI Components
from src.components.LeftSidebar import LeftSidebar
from src.components.TimeEntriesList import TimeEntriesList
from src.components.ProjectsList import ProjectsList
from src.components.TimeTracker import TimeTracker
from src.components.Timer import Timer


class MainFrame(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.config = parent.config

        # GUI components
        # MenuBar(self)
        sb_left = LeftSidebar(self)
        sb_left.pack(side="left", fill="y")

        tel = TimeEntriesList(self, app=self.parent)
        tel.pack(side='right', expand=True, fill='both')

        #proj_l = ProjectsList(self, self.parent)
        #proj_l.pack(side="top", fill="x")

        #tt = TimeTracker(self, self.parent)
        #tt.pack(side="bottom", fill="x")

        self.pack(fill="both", expand=True)
