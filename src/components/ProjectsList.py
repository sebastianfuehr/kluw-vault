from tkinter import ttk
from ..controller.project_service import ProjectService

class ProjectsList(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app

        project_columns = [
            'Name'
        ]

        projects = ProjectService.get_all(self.app.session)
        row_nbr = 0
        for project in projects:
            row_nbr += 1
            for col_nbr in range(len(project_columns)):
                lbl_project = ttk.Label(self, text=f"{project.name}")
                lbl_project.grid(row=row_nbr, column=col_nbr)