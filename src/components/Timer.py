# https://www.geeksforgeeks.org/create-countdown-timer-using-python-tkinter/

from tkinter import ttk

class Timer(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container

        self.state = 'Stopped'
        self.minutes_total = 25
        self.seconds_total = 0

        self.minutes_curr = self.minutes_total
        self.seconds_curr = self.seconds_total

        self.lbl_time_left = ttk.Label(self, text='00:00:00')
        self.lbl_time_left.pack()

        self.countdown()

        self.pack()

    def countdown(self):
        self.lbl_time_left['text'] = '{:02}:{:02}'.format(self.minutes_curr, self.seconds_curr)
        self.container.container.after(1000, self.countdown)

        if self.seconds_curr == 0:
            self.minutes_curr -= 1
            self.seconds_curr = 59
        else:
            self.seconds_curr -=1
