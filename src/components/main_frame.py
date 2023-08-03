"""A collection ov frames for displaying database entities."""
import ttkbootstrap as tb

from src.components.dashboard import StatsDashboard
from src.components.forms import ProjectCategoryForm, ProjectForm
from src.components.frames import ListFrame

# GUI Components
from src.components.left_sidebar import LeftSidebar
from src.components.navigation import ButtonPanel
from src.components.TimeEntriesList import TimeEntriesList
from src.components.views import CategoryDetailView, ProjectDetailView
from src.controller.project_category_service import ProjectCategoryService

# DB Services
from src.controller.project_service import ProjectService


class MainFrame(tb.Frame):
    """The visual entrypoint of the application. Everything related to
    building the GUI comes through here.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.app = parent
        self.config = parent.config

        self.tab_nav_str = tb.StringVar()
        self.tab_nav_key = tb.StringVar()  # The currently selected tab
        self.tab_nav_key.trace("w", self.build_tab_frame)
        self.central_frame = None

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.__build_gui_components()
        self.tab_nav_key.set(
            list(self.app.definitions.MAINFRAME_TABS_NAV["elements"].keys())[0]
        )

        self.pack(fill="both", expand=True)

    def __build_gui_components(self):
        """Construct the GUI elements of this component."""
        sb_left = LeftSidebar(self, self.parent)
        sb_left.grid(row=0, rowspan=3, column=0, sticky="nsew")
        self.parent.stats_sidebar = sb_left

        sidebar_sep = tb.Separator(self, orient="vertical")
        sidebar_sep.grid(row=0, rowspan=3, column=1, sticky="ns")

        tab_bar_sep = tb.Separator(self)
        tab_bar_sep.grid(row=1, column=2, sticky="ew")

        # Main tabs of the application
        self.tab_dashboard = StatsDashboard(self, app=self.parent)
        self.tab_time_entries = TimeEntriesList(self, app=self.parent)
        self.tab_projects = ListFrame(
            master=self,
            app=self.parent,
            db_service=ProjectService,
            db_session=self.parent.session,
            form_edit=ProjectForm,
            detail_view=ProjectDetailView,
            db_delete_item=ProjectService.delete,
        )
        self.tab_categories = ListFrame(
            master=self,
            app=self.parent,
            db_service=ProjectCategoryService,
            db_session=self.parent.session,
            form_edit=ProjectCategoryForm,
            detail_view=CategoryDetailView,
            db_delete_item=ProjectCategoryService.delete,
        )

        # Main navigation tabs
        tab_nav = ButtonPanel(
            parent=self,
            ttk_string_var=self.tab_nav_str,
            labels=self.app.definitions.MAINFRAME_TABS_NAV["elements"],
            styling=self.app.definitions.MAINFRAME_TABS_NAV,
            ttk_key_var=self.tab_nav_key,
        )
        tab_nav.grid(row=0, column=2, sticky="ew")
        tab_nav.buttons[0].select_handler()

    def build_tab_frame(self, *_args):
        """Will make the central frame which is currently visible
        invisible and puts the selected tab instead.
        """
        if self.central_frame:
            self.central_frame.grid_forget()
        match self.tab_nav_key.get():
            case "dashboard":
                self.central_frame = self.tab_dashboard
            case "time-entries":
                self.central_frame = self.tab_time_entries
            case "projects":
                self.central_frame = self.tab_projects
            case "categories":
                self.central_frame = self.tab_categories
        self.central_frame.grid(row=2, column=2, sticky="nsew")
        self.central_frame.update()
