import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math
from dateutil.parser import parse


class CustomFigure:

    @staticmethod
    def create_figure(values, labels, x_title, y_title, fontsize=20, dpi=600, group_size=3):
        """ Create a figure with subplots for the soil moisture data

        :param values: The values of the measurements
        :param labels: The labels for the graphs
        :param x_title: The x-axis title
        :param y_title: The y-axis title
        :param fontsize: The fontsize of the labels
        :return: The figure
        """
        count_subplots = math.ceil(len(values) / group_size)
        fig, axs = plt.subplots(count_subplots, figsize=(15, 20), dpi=dpi, sharex=True)
        fig.text(0.5, 0.04, x_title, ha='center', va='center', fontsize=20)
        fig.text(0.06, 0.5, y_title, ha='center', va='center', rotation='vertical', fontsize=fontsize)
        min_value = min(d['controlledproperty'] for sublist in values for d in sublist)
        max_value = max(d['controlledproperty'] for sublist in values for d in sublist)
        # Define the groups of measurements for each subplot

        groups = [values[i:i + group_size] for i in range(0, len(values), group_size)]

        for i, group in enumerate(groups):
            ax = axs[i]
            for j, measurement in enumerate(group):
                dates = [parse(d['datecreated']) for d in measurement]
                values = [d['controlledproperty'] for d in measurement]
                ax.plot(dates, values, label=labels[i * group_size + j])
            ax.legend(loc='upper left', fontsize=fontsize)
            ax.grid(True)
            ax.set_ylim(min_value, max_value)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y %H:%M'))
            ax.tick_params(axis='x', rotation=45, labelsize=fontsize)
            ax.tick_params(axis='y', labelsize=fontsize)

        return fig
