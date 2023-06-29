from tkinter import ttk
import time
from datetime import datetime
# Custom libraries
from ..model.time_entry import TimeEntry

class TimeTracker(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app

        self.curr_time_entry = None
        self.state = 'Ready'

        # Work session specific variables
        self.hours_curr = 0
        self.minutes_curr = 0
        self.seconds_curr = 0
        self.pause_hours_curr = 0
        self.pause_minutes_curr = 0
        self.pause_seconds_curr = 0

        self.current_time = ttk.Label(self, text='00:00:00!')
        self.current_time.pack()

        btn_start_session = ttk.Button(self,
                                       text='Start',
                                       command=self.bnt_start_clicked
            ).pack()
        btn_pause_session = ttk.Button(self,
                                       text='Pause',
                                       command=self.btn_pause_clicked
            ).pack()
        btn_end_session = ttk.Button(self,
                                     text='End',
                                     command=self.btn_end_clicked
            ).pack()

    def counting(self):
        self.current_time['text'] = self.get_timer_string()

        if self.state == 'Running':
            if self.seconds_curr == 60:
                self.minutes_curr += 1
                self.seconds_curr = 0
            else:
                self.seconds_curr +=1
            self.parent.parent.after(1000, self.counting)
        elif self.state == 'Paused':
            if self.pause_seconds_curr == 60:
                self.pause_minutes_curr += 1
                self.pause_seconds_curr = 0
            else:
                self.pause_seconds_curr +=1
            self.parent.parent.after(1000, self.counting)
        

    def bnt_start_clicked(self):
        print(f'{datetime.now()} Session started')
        
        if self.state == 'Ready':
            new_entry = TimeEntry(start=datetime.now())
            self.app.session.add(new_entry)
            self.app.session.commit()

            self.curr_time_entry = new_entry
        
        self.state = 'Running'
        self.counting()

    def btn_pause_clicked(self):
        print(f'{datetime.now()} Session paused')
        self.state = 'Paused'

    def btn_end_clicked(self):
        print(f'{datetime.now()} Session ended')
        self.state = 'Stopped'
    
    def get_timer_string(self):
        res = ''
        if self.hours_curr > 1:
            res = '{:02}:{:02}:{:02}'.format(
                self.hours_curr,
                self.minutes_curr,
                self.seconds_curr
            )
        else:
            res = '{:02}:{:02}'.format(self.minutes_curr, self.seconds_curr)

        pause_str = ''
        if self.pause_hours_curr > 1:
            pause_str = '(Pause: {:02}:{:02}:{:02})'.format(
                self.pause_hours_curr,
                self.pause_minutes_curr,
                self.pause_seconds_curr
            )
        elif self.pause_seconds_curr > 0 or self.pause_minutes_curr > 0:
            pause_str = '(Pause: {:02}:{:02})'.format(
                self.pause_minutes_curr,
                self.pause_seconds_curr
            )

        return res + pause_str