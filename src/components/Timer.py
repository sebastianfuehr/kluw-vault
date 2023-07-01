# https://www.geeksforgeeks.org/create-countdown-timer-using-python-tkinter/

import ttkbootstrap as tb

from ..controller.timer_controller import TimerController


class Timer(tb.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.timer_controller = TimerController()

        fps = 25
        self.framerate = int(1000/fps)
        self.state = 'off'

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.init_gui_components()

    def init_gui_components(self):
        self.lbl_time_display = tb.Label(
            master=self,
            text='0:00:00',
            anchor='center',
            font=('Helvetica', 22, 'bold')
        )
        self.lbl_time_display.grid(
            row=0, column=0, columnspan=2, sticky='ew', padx=10, pady=10
        )

        self.lbl_paused_time_display = tb.Label(
            master=self,
            text='0:00:00',
            anchor='center',
            font=('Helvetica', 12)
        )
        self.lbl_paused_time_display.grid(
            row=1, column=0, columnspan=2, sticky='ew', padx=10
        )

        self.btn_start_pause_resume = tb.Button(
            master=self,
            text='Start',
            command=self.start_handler,
            bootstyle='success'
        )
        self.btn_start_pause_resume.grid(
            row=2, column=0, sticky='ew', padx=10, pady=10
        )

        self.btn_stop = tb.Button(
            master=self,
            text='Stop',
            command=self.timer_controller.stop,
            bootstyle='danger',
            state='disabled'
        )
        self.btn_stop.grid(row=2, column=1, sticky='ew', padx=10, pady=10)

        self.btn_reset = tb.Button(
            master=self,
            text='Reset',
            command=self.reset_handler,
            bootstyle='secondary-link',
            state='disabled'
        )
        self.btn_reset.grid(row=3, column=0, columnspan=2)

    def start_handler(self):
        if self.state == 'off':
            self.timer_controller.start()
            self.state = 'on'
            self.update_display()
        elif self.state == 'on':
            self.timer_controller.pause()
            self.state = 'pause'
            self.update_display()
        elif self.state == 'pause':
            self.timer_controller.resume()
            self.state = 'on'
            self.update_display()
        self.update_buttons()

    def reset_handler(self):
        self.timer_controller.reset()
        self.state = 'off'
        self.update_buttons()
        self.lbl_time_display['text'] = '0:00:00'
        self.lbl_paused_time_display['text'] = '0:00:00'

    def update_buttons(self):
        if self.state == 'off':
            self.btn_start_pause_resume.configure(text='Start',
                                                  bootstyle='success')
            self.btn_stop.configure(state='disabled')
            self.btn_reset.configure(state='disabled')
        elif self.state == 'on':
            self.btn_start_pause_resume.configure(text='Pause',
                                                  bootstyle='info')
            self.btn_stop.configure(state='normal')
            self.btn_reset.configure(state='normal')
        elif self.state == 'pause':
            self.btn_start_pause_resume.configure(text='Resume',
                                                  bootstyle='success')

    def update_display(self):
        if self.state == 'on':
            elapsed = self.timer_controller.get_current_duration()
            self.lbl_time_display['text'] = str(elapsed).split('.', 2)[0]
            self.after(100, self.update_display)
        elif self.state == 'pause':
            elapsed = self.timer_controller.get_current_pause_duration()
            self.lbl_paused_time_display['text'] = str(elapsed).split('.', 2)[0]
            self.after(100, self.update_display)

    """
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
    """
