import logging
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
from sqlalchemy import select

from src.components.navigation import ButtonPanel
from ..model.time_entry import TimeEntry
from ..controller.time_entry_service import TimeEntryService
from ..controller.time_controller import TimeController
from .. components.frames import AutoLayoutFrame
from .. components.visuals import GraphTimePerDay, GraphTimesPerDay


class StatsDashboard(tb.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app

        self.has_content = False
        self.time_string = tb.StringVar(value=self.app.definitions.FILTER_PERIODS["elements"][4])
        self.time_string.trace("w", self.select_handler)

        self.preprocess_data()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        scrolled_frame = ScrolledFrame(self, autohide=True)
        scrolled_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame = AutoLayoutFrame(scrolled_frame, self.app.definitions.VIEW_DASHBOARD['grid-config'], self.app.definitions.VIEW_DASHBOARD['labels'])
        self.content_frame.pack(expand=True, fill='both', padx=25)
        self.content_frame.grid_columnconfigure((0, 1), weight=1)

        filter_panel = ButtonPanel(
            parent=self,
            ttk_string_var=self.time_string,
            labels=self.app.definitions.FILTER_PERIODS["elements"],
            styling=self.app.definitions.FILTER_PERIODS,
        )
        filter_panel.grid(row=0, column=0, sticky="ew")

    def preprocess_data(self):
        """Takes the current dataframe from DataController and prepares
        it for further use.
        """
        self.data_max = self.app.dc.time_entry_df

        ago_one_year = str((datetime.today() - timedelta(days=365)).date())
        ago_six_months = str((datetime.today() - timedelta(days=182)).date())
        ago_one_month = str((datetime.today() - timedelta(days=31)).date())
        ago_one_week = str((datetime.today() - timedelta(days=7)).date())
        self.data_one_year = self.data_max[
            self.data_max["Date"] > ago_one_year
        ]
        self.data_six_months = self.data_max[
            self.data_max["Date"] > ago_six_months
        ]
        self.data_one_month = self.data_max[
            self.data_max["Date"] > ago_one_month
        ]
        self.data_one_week = self.data_max[
            self.data_max["Date"] > ago_one_week
        ]

    def select_handler(self, *_args):
        # Select the right data set
        match self.time_string.get():
            case "Max":
                data = self.data_max
            case "1 Year":
                data = self.data_one_year
            case "6 Months":
                data = self.data_six_months
            case "Month":
                data = self.data_one_month
            case "Week":
                data = self.data_one_week

        self.build_gui_components(data)

    def build_gui_components(self, data):
        if len(self.data_max) == 0:
            return
        if self.has_content:
            self.graph_time_per_day.grid_forget()
        layout = self.app.definitions.VIEW_DASHBOARD
        # Group data
        tmp_data = data
        duration_per_day = tmp_data.groupby(pd.Grouper(key="Date", freq="D"))[
            "Duration"
        ].sum()
        duration_per_day = duration_per_day.reset_index()
        duration_per_day["Minutes"] = (
            duration_per_day["Duration"].dt.total_seconds() / 60 / 60
        )

        tmp_data = data
        project_times = tmp_data.groupby(["Project Name", "Date"])["Duration"].sum()
        project_times = project_times.unstack("Project Name").fillna(pd.Timedelta(0))

        GraphTimesPerDay(
            parent=self.content_frame,
            app=self.app,
            data=project_times,
            value_column_name=None
        ).grid(
            row=layout['graph_time_per_project_per_day']['row'],
            column=layout['graph_time_per_project_per_day']['col'],
            rowspan=layout['graph_time_per_project_per_day']['rowspan'],
            columnspan=layout['graph_time_per_project_per_day']['columnspan'],
            sticky=layout['graph_time_per_project_per_day']['sticky'],
            padx=layout['graph_time_per_project_per_day']['padx'],
            pady=layout['graph_time_per_project_per_day']['pady']
        )

        # Table - Overview panel
        self.overview_panel = OverviewPanel(self.content_frame, self.app, data)
        self.overview_panel.grid(row=1, column=0, sticky="nsew")

        # Graph - Total time per day
        self.graph_time_per_day = GraphTimePerDay(
            parent=self.content_frame,
            app=self.app,
            data=duration_per_day,
            value_column_name="Minutes"
        )
        self.graph_time_per_day.grid(
            row=layout['graph_time_per_day']['row'],
            column=layout['graph_time_per_day']['col'],
            rowspan=layout['graph_time_per_day']['rowspan'],
            columnspan=layout['graph_time_per_day']['columnspan'],
            sticky=layout['graph_time_per_day']['sticky'],
            padx=layout['graph_time_per_day']['padx'],
            pady=layout['graph_time_per_day']['pady']
        )

        self.has_content = True


class OverviewPanel(tb.Frame):
    def __init__(self, parent, app, data):
        super().__init__(master=parent)
        self.app = app
        self.data = data

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.calculate_values()
        self.build_gui_components()

    def calculate_values(self):
        goals = self.app.pcgsc.get_active_goals()
        weekday = datetime.today().weekday()
        total_goal_minutes = 0
        for goal in goals:
            if goal.get_weekday_minute_goal(weekday) > 0:
                total_goal_minutes += goal.get_weekday_minute_goal(weekday)

        goal_str = TimeController.seconds_to_string(total_goal_minutes * 60)
        self.goal_today_str = tb.StringVar(self, goal_str)
        curr_ratio = self.app.sc.total_time_today() / 60 / total_goal_minutes
        self.progress_today = tb.StringVar(
            self, f"{round(curr_ratio*100, 1)}%"
        )

    def build_gui_components(self):
        self.block_goal_today = OverviewPanelBlock(
            self, self.app, "GOAL TODAY", self.goal_today_str
        )
        self.block_goal_today.grid(row=0, column=0, sticky="nsew", padx=10)
        self.block_progress_today = OverviewPanelBlock(
            self, self.app, "PROGRESS", self.progress_today
        )
        self.block_progress_today.grid(row=0, column=1, sticky="nsew", padx=10)


class OverviewPanelBlock(tb.Frame):
    def __init__(self, parent, app, heading, value_str):
        super().__init__(master=parent)
        self.app = app
        self.value_str = value_str

        self.configure(borderwidth=1, relief="solid")

        lbl_heading = tb.Label(
            self, text=heading, font=(None, 14, "bold"), anchor="center"
        )
        lbl_heading.pack(side="top", fill="x", pady=(20, 0))

        lbl_value = tb.Label(
            self,
            text=value_str.get(),
            font=(None, 32, "bold"),
            anchor="center",
        )
        lbl_value.pack(side="top", fill="x", pady=20)
