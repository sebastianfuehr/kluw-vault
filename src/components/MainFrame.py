import ttkbootstrap as tb

# GUI Components
from src.components.LeftSidebar import LeftSidebar
from src.components.StatsDashboard import StatsDashboard
from src.components.TimeEntriesList import TimeEntriesList


class MainFrame(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.config = parent.config

        # GUI components
        # MenuBar(self)
        sb_left = LeftSidebar(self, self.parent)
        sb_left.pack(side="left", fill="y")
        self.parent.stats_sidebar = sb_left

        central_notebook = tb.Notebook(
            self
        )
        central_notebook.pack(side='right', expand=True, fill='both')

        tab_time_entries = TimeEntriesList(central_notebook, app=self.parent)
        central_notebook.add(tab_time_entries, text='Time Entries')

        tab_stats_dashboard = StatsDashboard(central_notebook, app=self.parent)
        central_notebook.add(tab_stats_dashboard, text='Dashboard')

        tab_projects = tb.Frame(central_notebook)
        central_notebook.add(tab_projects, text='Projects')

        tab_categories = tb.Frame(central_notebook)
        central_notebook.add(tab_categories, text='Categories')

        tab_settings = tb.Frame(central_notebook)
        central_notebook.add(tab_settings, text='Settings')

        #proj_l = ProjectsList(self, self.parent)
        #proj_l.pack(side="top", fill="x")

        self.pack(fill="both", expand=True)
