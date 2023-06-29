from tkinter import ttk

from src.model.project import Project
# GUI Components
from src.components.LeftSidebar import LeftSidebar
from src.components.TimeEntriesList import TimeEntriesList
from src.components.ProjectsList import ProjectsList
from src.components.TimeTracker import TimeTracker
from src.components.Timer import Timer

class MainFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.config = parent.config

        # GUI components
        # MenuBar(self)
        sb_l = LeftSidebar(self)
        sb_l.pack(side="left", fill="y")
        
        tel = TimeEntriesList(self, self.parent)
        tel.pack(side="top", fill="both")

        proj_l = ProjectsList(self, self.parent)
        proj_l.pack(side="top", fill="x")

        tt = TimeTracker(self, self.parent)
        tt.pack(side="bottom", fill="x")

        self.pack(fill="both", expand=True)