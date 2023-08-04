from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Tuple

import pandas as pd
import ttkbootstrap as tb
from PIL import Image, ImageTk
from ttkbootstrap.scrolled import ScrolledFrame

from src.components.navigation import ButtonPanel

from ..components.frames import AutoLayoutFrame
from ..components.visuals import GraphTimePerDay, GraphTimesPerDay
from ..controller.time_controller import TimeController

if TYPE_CHECKING:
    from app import App


class StatsDashboard(tb.Frame):  # type: ignore
    def __init__(self, parent: tb.Frame, app: "App") -> None:
        super().__init__(parent)
        self.parent = parent
        self.app = app

        self.has_content = False
        self.time_string = tb.StringVar(
            value=self.app.definitions.FILTER_PERIODS["elements"][4]
        )
        self.time_string.trace("w", self.select_handler)

        self.preprocess_data()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        scrolled_frame = ScrolledFrame(self, autohide=True)
        scrolled_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame = AutoLayoutFrame(
            scrolled_frame,
            self.app.definitions.VIEW_DASHBOARD["grid-config"],
            self.app.definitions.VIEW_DASHBOARD["labels"],
        )
        self.content_frame.pack(expand=True, fill="both", padx=25)
        self.content_frame.grid_columnconfigure((0, 1), weight=1)

        filter_panel = ButtonPanel(
            parent=self,
            ttk_string_var=self.time_string,
            labels=self.app.definitions.FILTER_PERIODS["elements"],
            styling=self.app.definitions.FILTER_PERIODS,
        )
        filter_panel.grid(row=0, column=0, sticky="ew")

    def preprocess_data(self) -> None:
        """Takes the current dataframe from DataController and prepares
        it for further use.
        """
        self.data_max: pd.DataFrame = self.app.dc.time_entry_df

        ago_one_year = str((datetime.today() - timedelta(days=365)).date())
        ago_six_months = str((datetime.today() - timedelta(days=182)).date())
        ago_one_month = str((datetime.today() - timedelta(days=31)).date())
        ago_one_week = str((datetime.today() - timedelta(days=7)).date())
        self.data_one_year = self.data_max[self.data_max["Date"] > ago_one_year]
        self.data_six_months = self.data_max[self.data_max["Date"] > ago_six_months]
        self.data_one_month = self.data_max[self.data_max["Date"] > ago_one_month]
        self.data_one_week = self.data_max[self.data_max["Date"] > ago_one_week]

    def select_handler(self, *_args: int) -> None:
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

    def build_gui_components(self, data: pd.DataFrame) -> None:
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

        # Graph - Total time per project per day
        GraphTimesPerDay(
            parent=self.content_frame,
            app=self.app,
            data=project_times,
            value_column_name=None,
        ).grid(
            row=layout["graph_time_per_project_per_day"]["row"],
            column=layout["graph_time_per_project_per_day"]["col"],
            rowspan=layout["graph_time_per_project_per_day"]["rowspan"],
            columnspan=layout["graph_time_per_project_per_day"]["columnspan"],
            sticky=layout["graph_time_per_project_per_day"]["sticky"],
            padx=layout["graph_time_per_project_per_day"]["padx"],
            pady=layout["graph_time_per_project_per_day"]["pady"],
        )

        # Table - Overview panel
        self.overview_panel = OverviewPanel(self.content_frame, self.app, data)
        self.overview_panel.grid(row=1, column=0, sticky="nsew")

        # Medal score
        self.medal_score = MedalScore(self.content_frame, self.app, self.data_max)
        self.medal_score.grid(
            row=layout["medal_score"]["row"],
            column=layout["medal_score"]["col"],
            rowspan=layout["medal_score"]["rowspan"],
            columnspan=layout["medal_score"]["columnspan"],
            sticky=layout["medal_score"]["sticky"],
            padx=layout["medal_score"]["padx"],
            pady=layout["medal_score"]["pady"],
        )

        # Graph - Total time per day
        self.graph_time_per_day: GraphTimePerDay = GraphTimePerDay(
            parent=self.content_frame,
            app=self.app,
            data=duration_per_day,
            value_column_name="Minutes",
        )
        self.graph_time_per_day.grid(
            row=layout["graph_time_per_day"]["row"],
            column=layout["graph_time_per_day"]["col"],
            rowspan=layout["graph_time_per_day"]["rowspan"],
            columnspan=layout["graph_time_per_day"]["columnspan"],
            sticky=layout["graph_time_per_day"]["sticky"],
            padx=layout["graph_time_per_day"]["padx"],
            pady=layout["graph_time_per_day"]["pady"],
        )

        self.has_content = True


class OverviewPanel(tb.Frame):  # type: ignore
    def __init__(self, parent: tb.Frame, app: "App", data: pd.DataFrame) -> None:
        super().__init__(master=parent)
        self.app = app
        self.data = data
        self.tr = app.definitions.tr

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.calculate_values()
        self.build_gui_components()

    def calculate_values(self) -> None:
        goals = self.app.pcgsc.get_active_goals()
        weekday = datetime.today().weekday()
        total_goal_minutes = 0
        for goal in goals:
            if goal.get_weekday_minute_goal(weekday) > 0:
                total_goal_minutes += goal.get_weekday_minute_goal(weekday)

        goal_str = TimeController.seconds_to_string(total_goal_minutes * 60)
        self.goal_today_str = tb.StringVar(self, goal_str)
        curr_ratio = self.app.sc.total_time_today() / 60 / total_goal_minutes
        self.progress_today = tb.StringVar(self, f"{round(curr_ratio*6, 1)}%")

    def build_gui_components(self) -> None:
        self.block_goal_today = OverviewPanelBlock(
            self, self.app, self.tr("GOAL TODAY"), self.goal_today_str
        )
        self.block_goal_today.grid(row=0, column=0, sticky="nsew", padx=10)
        self.block_progress_today = OverviewPanelBlock(
            self, self.app, self.tr("PROGRESS"), self.progress_today
        )
        self.block_progress_today.grid(row=0, column=1, sticky="nsew", padx=10)


class OverviewPanelBlock(tb.Frame):  # type: ignore
    def __init__(
        self, parent: tb.Frame, app: "App", heading: str, value_str: tb.StringVar
    ) -> None:
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


class MedalScore(tb.Frame):  # type: ignore
    def __init__(self, parent: tb.Frame, app: "App", data_max: pd.DataFrame):
        super().__init__(master=parent)
        self.app = app
        self.data_max = data_max
        self.outline_color = "white"

        width = 550
        height = 300
        self.canvas = tb.Canvas(self, width=width, height=height)
        self.canvas.pack(side="top")

        total_bronze, total_silver, total_gold = self.calculate_values()
        self.draw_image(width, height, total_bronze, total_silver, total_gold)

    def draw_image(
        self,
        width: int,
        height: int,
        total_bronze: int,
        total_silver: int,
        total_gold: int,
    ) -> None:
        pedestal_width = width * 0.7 / 3
        center_bronze = width / 6
        center_gold = width / 6 * 3
        center_silver = width / 6 * 5
        height_bronze = height * 0.35
        height_gold = height * 0.55
        height_silver = height * 0.45

        self.canvas.create_line(
            (0, height), (width, height), width=2, fill=self.outline_color
        )

        # Draw pedestal
        self.canvas.create_rectangle(
            center_bronze - pedestal_width / 2,
            height - height_bronze,
            center_bronze + pedestal_width / 2,
            height,
            fill=self.outline_color,
        )
        self.canvas.create_rectangle(
            center_gold - pedestal_width / 2,
            height - height_gold,
            center_gold + pedestal_width / 2,
            height,
            fill=self.outline_color,
        )
        self.canvas.create_rectangle(
            center_silver - pedestal_width / 2,
            height - height_silver,
            center_silver + pedestal_width / 2,
            height,
            fill=self.outline_color,
        )

        # Medal icons
        icon_size = 160

        img_bronze = ImageTk.PhotoImage(
            Image.open(
                f"{self.app.definitions.APP_ROOT_DIR}/assets/icons/medal-bronze.png"
            ).resize((icon_size, icon_size))
        )
        self.img_bronze = img_bronze
        self.canvas.create_image(
            center_bronze,
            height - height_bronze - icon_size / 3,
            anchor=tb.CENTER,
            image=img_bronze,
        )

        img_gold = ImageTk.PhotoImage(
            Image.open(
                f"{self.app.definitions.APP_ROOT_DIR}/assets/icons/medal-gold.png"
            ).resize((icon_size, icon_size))
        )
        self.img_gold = img_gold
        self.canvas.create_image(
            center_gold,
            height - height_gold - icon_size / 3,
            anchor=tb.CENTER,
            image=img_gold,
        )

        img_silver = ImageTk.PhotoImage(
            Image.open(
                f"{self.app.definitions.APP_ROOT_DIR}/assets/icons/medal-silver.png"
            ).resize((icon_size, icon_size))
        )
        self.img_silver = img_silver
        self.canvas.create_image(
            center_silver,
            height - height_silver - icon_size / 3,
            anchor=tb.CENTER,
            image=img_silver,
        )

        # Draw text values
        self.canvas.create_text(
            center_bronze,
            height - height_bronze / 2 + 10,
            anchor=tb.CENTER,
            font=(None, 24, "bold"),
            text=total_bronze,
        )
        self.canvas.create_text(
            center_gold,
            height - height_gold / 2,
            anchor=tb.CENTER,
            font=(None, 34, "bold"),
            text=total_gold,
        )
        self.canvas.create_text(
            center_silver,
            height - height_silver / 2 + 5,
            anchor=tb.CENTER,
            font=(None, 28, "bold"),
            text=total_silver,
        )

    def calculate_values(self) -> Tuple[int, int, int]:
        # Group data
        tmp_data = self.data_max
        duration_per_day = tmp_data.groupby(pd.Grouper(key="Date", freq="D"))[
            "Duration"
        ].sum()
        duration_per_day = duration_per_day.reset_index()
        duration_per_day["Minutes"] = (
            duration_per_day["Duration"].dt.total_seconds() / 60
        )

        # Calculate number of medals
        column = duration_per_day["Minutes"]
        total_bronze = column[
            column > self.app.definitions.MEDAL_TH_BRONZE / 60
        ].count()
        total_silver = column[
            column > self.app.definitions.MEDAL_TH_SILVER / 60
        ].count()
        total_gold = column[column > self.app.definitions.MEDAL_TH_GOLD / 60].count()
        return total_bronze, total_silver, total_gold
