import ttkbootstrap as tb
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from sqlalchemy import select

from ..model.time_entry import TimeEntry
from ..controller.time_entry_service import TimeEntryService


class StatsDashboard(tb.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app

        """
        self.data = pd.read_sql(
            sql=select(TimeEntry),
            con=self.app.db_engine
        )
        """

        entries = TimeEntryService.get_all(self.app.session).all()
        row_data = [entry.to_list() for entry in entries]
        self.data = pd.DataFrame(row_data, columns=TimeEntry.get_column_names())[['Date', 'Duration']]
        self.data['Date'] = pd.to_datetime(self.data['Date'])

        self.build_gui_components()

    def build_gui_components(self):
        # Figure
        figure = plt.Figure()
        axis = figure.add_subplot(111)

        # Graph
        tmp_data = self.data
        data_by_date = tmp_data.groupby(pd.Grouper(key='Date', freq='D'))['Duration'].sum()
        data_by_date = data_by_date.reset_index()
        data_by_date['Minutes'] = data_by_date['Duration'].dt.total_seconds() / 60
        axis.plot(data_by_date['Date'], data_by_date['Minutes'])
        axis.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        figure.autofmt_xdate()

        # Widget
        fig_widget = FigureCanvasTkAgg(figure, master=self)
        fig_widget.get_tk_widget().pack()
