# https://www.geeksforgeeks.org/create-countdown-timer-using-python-tkinter/

import ttkbootstrap as tb

from ..controller.timer_controller import TimerController
from ..controller.time_controller import TimeController as tc


class Timer(tb.Frame):
    def __init__(self, parent, app, new_entry_var):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.new_entry_var = new_entry_var
        self.timer_controller = TimerController()

        self.state = "off"

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.init_gui_components()

    def init_gui_components(self):
        self.lbl_time_display = tb.Label(
            master=self,
            text="0h 0m 0s",
            anchor="center",
            font=("Helvetica", 22, "bold"),
        )
        self.lbl_time_display.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10
        )

        self.lbl_paused_time_display = tb.Label(
            master=self,
            text="0h 0m 0s",
            anchor="center",
            font=("Helvetica", 12),
        )
        self.lbl_paused_time_display.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=10
        )

        self.btn_start_pause_resume = tb.Button(
            master=self,
            text="Start",
            command=self.start_handler,
            bootstyle="success",
        )
        self.btn_start_pause_resume.grid(
            row=2, column=0, sticky="ew", padx=10, pady=10
        )

        self.btn_stop = tb.Button(
            master=self,
            text="Stop",
            command=self.stop_handler,
            bootstyle="danger",
            state="disabled",
        )
        self.btn_stop.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

        self.btn_reset = tb.Button(
            master=self,
            text="Reset",
            command=self.reset_handler,
            bootstyle="secondary-link",
            state="disabled",
        )
        self.btn_reset.grid(row=3, column=0, columnspan=2)

    def start_handler(self):
        if self.state == "off":
            self.new_entry_var.set(True)
            self.timer_controller.start()
            self.parent.start_new_entry()
            self.state = "on"
            self.update_display()
        elif self.state == "on":
            self.timer_controller.pause()
            self.state = "pause"
            self.update_display()
        elif self.state == "pause":
            curr_pause_duration = self.timer_controller.resume()
            self.parent.resume_entry(curr_pause_duration)
            self.state = "on"
            self.update_display()
        self.update_buttons()

    def stop_handler(self):
        self.timer_controller.stop()
        self.state = "stopped"
        self.parent.stop_entry(self.timer_controller.get_current_duration())
        self.update_buttons()

    def reset_handler(self):
        self.new_entry_var.set(False)
        self.timer_controller.reset()
        self.parent.start_new_entry()
        self.state = "off"
        self.update_buttons()
        self.lbl_time_display["text"] = "0:00:00"
        self.lbl_paused_time_display["text"] = "0:00:00"

    def update_buttons(self):
        if self.state == "off":
            self.btn_start_pause_resume.configure(
                text="Start", state="normal", bootstyle="success"
            )
            self.btn_stop.configure(state="disabled")
            self.btn_reset.configure(
                state="disabled", bootstyle="secondary-link"
            )
        elif self.state == "on":
            self.btn_start_pause_resume.configure(
                text="Pause", bootstyle="info"
            )
            self.btn_stop.configure(state="normal")
            self.btn_reset.configure(state="normal")
        elif self.state == "pause":
            self.btn_start_pause_resume.configure(
                text="Resume", bootstyle="success"
            )
        elif self.state == "stopped":
            self.btn_start_pause_resume.configure(state="disabled")
            self.btn_stop.configure(state="disabled")
            self.btn_reset.configure(bootstyle="success-link")

    def update_display(self):
        if self.state == "on":
            elapsed = self.timer_controller.get_current_duration()
            self.lbl_time_display["text"] = tc.timedelta_to_string(elapsed)
            self.after(100, self.update_display)
            self.app.stats_sidebar.update_total_time(elapsed)
        elif self.state == "pause":
            elapsed = self.timer_controller.get_current_pause_duration()
            self.lbl_paused_time_display["text"] = tc.timedelta_to_string(
                elapsed
            )
            self.after(100, self.update_display)
