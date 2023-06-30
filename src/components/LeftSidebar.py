import ttkbootstrap as tb
from datetime import timedelta


class LeftSidebar(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.config = parent.config

        msg_user = f"Currently logged in as {self.config['User']['last_login_username']}"
        lbl_username = tb.Label(self, text=msg_user)
        lbl_username.pack(side="bottom")

        seconds_today = self.parent.parent.sc.total_time_today()
        lbl_progress = tb.Label(self, text=str(timedelta(seconds=seconds_today)))
        lbl_progress.pack(side='top')
