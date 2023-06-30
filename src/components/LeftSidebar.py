import ttkbootstrap as tb


class LeftSidebar(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.config = parent.config

        lbl_username = tb.Label(self, text=f"Currently logged in as {self.config['User']['last_login_username']}")
        lbl_username.pack(side="bottom")
