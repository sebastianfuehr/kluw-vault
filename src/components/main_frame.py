import ttkbootstrap as tb

# Custom modules
from config.definitions import *
# GUI Components
from src.components.left_sidebar import LeftSidebar
from src.components.dashboard import StatsDashboard
from src.components.TimeEntriesList import TimeEntriesList
from src.components.ProjectsList import ProjectsList
from src.components.CategoryGoalsList import CategoryGoalsList


class MainFrame(tb.Frame):
    """The visual entrypoint of the application. Everything related to
    building the GUI comes through here.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.config = parent.config

        self.tab_nav_str = tb.StringVar() # The currently selected tab
        self.tab_nav_str.trace('w', self.build_tab_frame)
        self.central_frame = None

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.__build_gui_components()
        self.pack(fill="both", expand=True)

    def __build_gui_components(self):
        """Construct the GUI elements of this component.
        """
        sb_left = LeftSidebar(self, self.parent)
        sb_left.grid(row=0, rowspan=3, column=0, sticky='ns')
        self.parent.stats_sidebar = sb_left

        sidebar_sep = tb.Separator(self, orient='vertical')
        sidebar_sep.grid(row=0, rowspan=3, column=1, sticky='ns')

        tab_nav = TabNavigationPanel(self, self.tab_nav_str)
        tab_nav.grid(row=0, column=2, sticky='ew')

        tab_bar_sep = tb.Separator(self)
        tab_bar_sep.grid(row=1, column=2, sticky='ew')

        # Main tabs of the application
        self.tab_dashboard = StatsDashboard(self, app=self.parent)
        self.tab_time_entries = TimeEntriesList(self, app=self.parent)
        self.tab_projects = ProjectsList(self, app=self.parent)
        self.tab_categories = CategoryGoalsList(self, app=self.parent)

        # Set open tab upon startup
        self.tab_nav_str.set(MAINFRAME_TABS_NAV['elements'][0])

    def build_tab_frame(self, *args):
        """Will make the central frame which is currently visible
        invisible and puts the selected tab instead.
        """
        if self.central_frame:
            self.central_frame.grid_forget()
        match self.tab_nav_str.get():
            case 'Dashboard': 
                self.central_frame = self.tab_dashboard
            case 'Time Entries': 
                self.central_frame = self.tab_time_entries
            case 'Projects':
                self.central_frame = self.tab_projects
            case 'Categories':
                self.central_frame = self.tab_categories
        self.central_frame.grid(row=2, column=2, sticky='nsew')


class TabNavigationPanel(tb.Frame): # pylint: disable=too-many-ancestors
    """The navigation panel containing the main tabs of the
    application.
    """
    def __init__(self, parent, tab_nav_str):
        super().__init__(master=parent)

        self.buttons = []
        for tab in MAINFRAME_TABS_NAV['elements']:
            self.buttons.append(TabTextButton(
                master=self,
                text=tab,
                tab_nav_str=tab_nav_str,
                button_group=self.buttons
            ))


class TabTextButton(tb.Label): # pylint: disable=too-many-ancestors
    """
    Parameters
    ----------
    button_group: list(TabTextButton)
        The button group this button belongs to. When the button is
        highlighted, all other buttons of the same group are unselected
        via the unselect() function.
    """
    def __init__(self, master, text, tab_nav_str, button_group):
        colors = MAINFRAME_TABS_NAV['colors']
        super().__init__(
            master=master,
            text=text,
            foreground=colors['text'],
            font=MAINFRAME_TABS_NAV['font']
        )
        self.bind('<Button-1>', self.select_handler)

        self.button_group = button_group
        self.text = text
        self.tab_nav_str = tab_nav_str

        self.pack(
            side='left',
            padx=MAINFRAME_TABS_NAV['padx'],
            pady=MAINFRAME_TABS_NAV['pady']
        )

    def select_handler(self, *_args):
        """Callback method for when the label is clicked on.
        """
        self.tab_nav_str.set(self.text)
        for button in self.button_group:
            button.unselect()
        self.configure(foreground=MAINFRAME_TABS_NAV['colors']['highlight'])

    def unselect(self):
        """Resets the text color."""
        self.configure(foreground=MAINFRAME_TABS_NAV['colors']['text'])
