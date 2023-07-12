import ttkbootstrap as tb

from config.definitions import *
from src.controller.project_category_service import ProjectCategoryService
from src.components.navigation import ButtonPanel


class TabFrame(tb.Frame):
    """A generic class for tabs.

    Parameters
    ----------
    """

    def __init__(self, master):
        super().__init__(master=master)
        self.registered_components = []

    def register(self, component):
        self.registered_components.append(component)

    def refresh(self):
        """Refreshes all registered components inside this frame.

        This method is invoked by whichever parent holds those tab
        frames.
        """
        for component in self.registered_components:
            component.refresh()


class TabFrameList(TabFrame):
    def __init__(self, master, db_service, db_session):
        super().__init__(master=master)
        self.db_service = db_service
        self.db_session = db_session

        self.category_str_var = tb.StringVar()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=7)
        self.grid_rowconfigure(0, weight=1)

        self.build_gui_components()

    def build_gui_components(self):
        """Create the GUI elements for this component.
        """
        self.frm_item_list = None

        for separator in TAB_FRAME_LIST['separators']:
            sep_new = tb.Separator(self, orient=separator['orient'])
            sep_new.grid(
                row=separator['row'],
                column=separator['col'],
                rowspan=separator['rowspan'],
                sticky=separator['sticky']
            )

        btn_new_item = tb.Button(self, text='New', bootstyle='success')
        btn_new_item.grid(row=2, column=0, pady=25)

        self.register(self)
        self.refresh()

    def refresh(self):
        list_layout = TAB_FRAME_LIST['sidebar']
        items = self.db_service.get_all(self.db_session).all()
        self.frm_item_list = ButtonPanel(
            self,
            self.category_str_var,
            labels=[item.name for item in items],
            styling=LIST_ITEM
        )
        self.frm_item_list.grid(
            row=list_layout['row'],
            column=list_layout['col'],
            sticky=list_layout['sticky']
        )


class CategoriesListTab(TabFrameList):
    def __init__(self, master, db_session):
        super().__init__(
            master=master,
            db_service=ProjectCategoryService,
            db_session=db_session
        )


class ProjectsListTab(TabFrameList):
    def __init__(self, master):
        pass

