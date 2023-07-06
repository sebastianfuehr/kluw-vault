import ttkbootstrap as tb
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
from sqlalchemy import select

from config.definitions import *
from ..model.time_entry import TimeEntry
from ..controller.time_entry_service import TimeEntryService


class StatsDashboard(tb.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app

        self.has_content = False
        self.time_string = tb.StringVar(value=FILTER_PERIODS[4])
        self.time_string.trace('w', self.build_gui_components)

        self.update_data()

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((1, 2, 3, 4), weight=1)

        filter_panel = FilterPanel(self, self.time_string)
        filter_panel.grid(row=0, column=0, columnspan=4, sticky='ew')

        """
        self.data = pd.read_sql(
            sql=select(TimeEntry),
            con=self.app.db_engine
        )
        """

    def update_data(self):
        entries = TimeEntryService.get_all(self.app.session).all()
        row_data = [entry.to_list() for entry in entries]
        self.data_max = pd.DataFrame(row_data, columns=TimeEntry.get_column_names())
        self.data_max['Date'] = pd.to_datetime(self.data_max['Date'], errors='coerce')

        # self.data_max[self.data_max['Date'] > '2023-07-04']
        ago_one_year = str((datetime.today() - timedelta(days=365)).date())
        ago_six_months = str((datetime.today() - timedelta(days=182)).date())
        ago_one_month = str((datetime.today() - timedelta(days=31)).date())
        ago_one_week = str((datetime.today() - timedelta(days=7)).date())
        self.data_one_year = self.data_max[self.data_max['Date'] > ago_one_year]
        self.data_six_months = self.data_max[self.data_max['Date'] > ago_six_months]
        self.data_one_month = self.data_max[self.data_max['Date'] > ago_one_month]
        self.data_one_week = self.data_max[self.data_max['Date'] > ago_one_week]

    def build_gui_components(self, *args):
        if self.has_content:
            self.graph_time_per_day.grid_forget()

        match self.time_string.get():
            case 'Max': data = self.data_max
            case '1 Year': data = self.data_one_year
            case '6 Months': data = self.data_six_months
            case 'Month': data = self.data_one_month
            case 'Week': data = self.data_one_week

        self.graph_time_per_day = GraphTimePerDay(self, self.app, data)
        self.graph_time_per_day.grid(row=2, column=0, columnspan=2, sticky='nsew')

        self.overview_panel = OverviewPanel(self, self.app, data)
        self.overview_panel.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.has_content = True


class OverviewPanel(tb.Frame):
    def __init__(self, parent, app, data):
        super().__init__(master=parent)
        self.app = app
        self.data = data

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        lbl_heading = tb.Label(
            self,
            text='Overview',
            font=(None, DASHBOARD_HEADING_SIZE, 'bold'),
            anchor='center'
        )
        lbl_heading.grid(row=0, column=0, columnspan=4, sticky='ew', pady=10)

        self.calculate_values()
        self.build_gui_components()

    def calculate_values(self):
        self.goal_today_str = tb.StringVar(self, f'{100}m')
        self.progress_today = tb.StringVar(self, f'{50}%')

    def build_gui_components(self):
        self.block_goal_today = OverviewPanelBlock(self, self.app, 'GOAL TODAY', self.goal_today_str)
        self.block_goal_today.grid(row=1, column=0, sticky='nsew', padx=10)
        self.block_progress_today = OverviewPanelBlock(self, self.app, 'PROGRESS', self.progress_today)
        self.block_progress_today.grid(row=2, column=0, sticky='nsew', padx=10)


class OverviewPanelBlock(tb.Frame):
    def __init__(self, parent, app, heading, value_str):
        super().__init__(master=parent)
        self.app = app
        self.value_str = value_str

        self.configure(borderwidth=1, relief='solid')

        lbl_heading = tb.Label(
            self,
            text=heading,
            font=(None, 14, 'bold'),
            anchor='center'
        )
        lbl_heading.pack(side='top', fill='x', pady=(20, 0))

        lbl_value = tb.Label(
            self,
            text=value_str.get(),
            font=(None, 32, 'bold'),
            anchor='center'
        )
        lbl_value.pack(side='top', fill='x', pady=20)


class GraphTimePerDay(tb.Frame):
    def __init__(self, parent, app, data):
        super().__init__(master=parent)
        self.app = app
        self.data = data

        lbl_heading = tb.Label(
            self,
            text='Time per Day',
            font=(None, DASHBOARD_HEADING_SIZE, 'bold'),
            anchor='center'
        )
        lbl_heading.pack(side='top', fill='x', pady=10)

        # Figure
        figure = plt.Figure()
        figure.subplots_adjust(left=0.02, bottom=0.1, right=1, top=1)
        figure.patch.set_facecolor(self.app.style.colors.bg)
        figure.autofmt_xdate()

        # Graph
        tmp_data = self.data
        data_by_date = tmp_data.groupby(pd.Grouper(key='Date', freq='D'))['Duration'].sum()
        data_by_date = data_by_date.reset_index()
        data_by_date['Minutes'] = data_by_date['Duration'].dt.total_seconds() / 60 / 60
        data_by_date['Average'] = data_by_date['Minutes'].mean()
        axis = figure.add_subplot(111)
        line = axis.plot(data_by_date['Date'], data_by_date['Minutes'])[0]
        line_avg = axis.plot(data_by_date['Date'], data_by_date['Average'], linestyle='dashed', label='Average per Day')[0]
        axis.legend(loc='upper right')
        line.set_color(HIGHLIGHT_COLOR)

        axis.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        axis.set_ylim(ymin=0)
        axis.set_facecolor(self.app.style.colors.bg)
        for side in ['left', 'bottom']:
            axis.spines[side].set_color('white')
        for side in ['right', 'top']:
            axis.spines[side].set_color(self.app.style.colors.bg)

        # Ticks
        axis.tick_params(axis='x', colors='white')
        axis.tick_params(axis='y', colors='white')

        # Widget
        fig_widget = FigureCanvasTkAgg(figure, master=self)
        fig_widget.get_tk_widget().pack(side='top', fill='both')


class FilterPanel(tb.Frame):
    def __init__(self, parent, time_string):
        super().__init__(master=parent)
        self.buttons = [FilterTextButton(self, text, time_string) for text in FILTER_PERIODS]
        time_string.trace('w', self.__unselect_filter_buttons)

    def __unselect_filter_buttons(self, *args):
        [button.unselect() for button in self.buttons]


class FilterTextButton(tb.Label):
    def __init__(self, parent, text, time_string):
        super().__init__(master=parent, text=text, foreground=TEXT_COLOR)
        self.pack(side='right', padx=10, pady=10)
        self.bind('<Button-1>', self.__select_handler)

        self.text = text
        self.time_string = time_string

        if time_string.get() == text:
            self.__select_handler()

    def __select_handler(self, event=None):
        self.time_string.set(self.text)
        self.configure(foreground=HIGHLIGHT_COLOR)

    def unselect(self):
        self.configure(foreground=TEXT_COLOR)
