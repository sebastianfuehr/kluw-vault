"""A collection of graphs for the time journal."""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ttkbootstrap as tb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphTimePerDay(tb.Frame):
    def __init__(
        self, parent, app, data, value_column_name: str, date_column_name="Date"
    ):
        """Creates a line graph to depict time series data in addition
        to an average value line.

        Parameters
        ----------
        value_column_name : str
            The name of the column to plot over time.
        date_column_name : str
            The name of the column which contains the dates.
        """
        super().__init__(master=parent)
        self.app = app
        self.data = data

        # Figure
        figure = plt.Figure()
        figure.subplots_adjust(left=0.05, bottom=0.01, right=1, top=1)
        figure.patch.set_facecolor(self.app.style.colors.bg)
        figure.autofmt_xdate()

        # Graph
        data_by_date = self.data
        data_by_date["Average"] = data_by_date[value_column_name].mean()
        axis = figure.add_subplot(111)
        line = axis.plot(
            data_by_date[date_column_name], data_by_date[value_column_name]
        )[0]
        line_avg = axis.plot(
            data_by_date[date_column_name],
            data_by_date["Average"],
            linestyle="dashed",
            label="Average",
        )[0]
        axis.legend(loc="upper right")
        line.set_color(self.app.definitions.COLORS["highlight"])

        axis.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        axis.set_ylim(ymin=0)
        axis.set_facecolor(self.app.style.colors.bg)
        for side in ["left", "bottom"]:
            axis.spines[side].set_color("white")
        for side in ["right", "top"]:
            axis.spines[side].set_color(self.app.style.colors.bg)

        # Ticks
        axis.tick_params(axis="x", colors="white")
        axis.tick_params(axis="y", colors="white")

        # Widget
        fig_widget = FigureCanvasTkAgg(figure, master=self)
        fig_widget.get_tk_widget().pack(side="top", fill="both")


class GraphTimesPerDay(tb.Frame):
    def __init__(
        self, parent, app, data, value_column_name: str, date_column_name="Date"
    ):
        """Creates a line graph to depict time series data in addition
        to an average value line.

        Parameters
        ----------
        value_column_name : str
            The name of the column to plot over time.
        date_column_name : str
            The name of the column which contains the dates.
        """
        super().__init__(master=parent)
        self.app = app
        self.data = data

        # Figure
        figure = plt.Figure()
        figure.subplots_adjust(left=0.05, bottom=0.01, right=1, top=1)
        figure.patch.set_facecolor(self.app.style.colors.bg)
        figure.autofmt_xdate()

        # Graph
        data_by_date = self.data
        axis = figure.add_subplot(111)
        for col, data in data.items():
            axis.plot(data, label=col)
        axis.legend(loc="upper left")

        axis.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        axis.set_ylim(ymin=0)
        axis.set_facecolor(self.app.style.colors.bg)
        for side in ["left", "bottom"]:
            axis.spines[side].set_color("white")
        for side in ["right", "top"]:
            axis.spines[side].set_color(self.app.style.colors.bg)

        # Ticks
        axis.tick_params(axis="x", colors="white")
        axis.tick_params(axis="y", colors="white")

        # Widget
        fig_widget = FigureCanvasTkAgg(figure, master=self)
        fig_widget.get_tk_widget().pack(side="top", fill="both", padx=10, pady=10)
