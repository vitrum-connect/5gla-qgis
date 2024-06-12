import math

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from dateutil.parser import parse

from ..custom_logger import CustomLogger


class SoilMoistureFigure:
    """ CustomFigure class to create soil moisture figures

    """

    @staticmethod
    def create_figure(values, labels, group_size=1):
        """ Create a figure with subplots for the soil moisture data

        :param values: The values of the measurements
        :param labels: The labels for the graphs
        :param group_size: The group size of the measurements for each subplot
        :return: The figure
        """
        x_title = "Date"
        y_title = "Soil Moisture [%]"
        dpi = 800
        font_size = 20
        logger = CustomLogger()

        if len(values) == 0 or len(labels) == 0:
            logger.log_warning('The values and/or labels are empty')
            return None
        if values is None or labels is None:
            logger.log_warning('The values and/or labels are None')
            return None
        if not (len(values) // group_size) >= 1:
            logger.log_warning('The number of subplots is higher than the number of Axes')
            return None

        count_subplots = math.ceil(len(values) // group_size)
        # Create the figure and the subplots. If there is only one subplot, the axs is not a numpy array
        fig, axs = plt.subplots(count_subplots, figsize=(15, 20), dpi=dpi, sharex='col')
        fig.text(0.5, 0.04, x_title, ha='center', va='center', fontsize=font_size)
        fig.text(0.06, 0.5, y_title, ha='center', va='center', rotation='vertical', fontsize=font_size)
        min_value = min(d['controlledproperty'] for sublist in values for d in sublist) - 1
        max_value = max(d['controlledproperty'] for sublist in values for d in sublist) + 1
        if not isinstance(axs, np.ndarray):
            axs = [axs]
        groups = [values[i:i + group_size] for i in range(0, len(values), group_size)]
        for i, group in enumerate(groups):
            ax = axs[i]
            for j, measurement in enumerate(group):
                dates = [parse(d['datecreated']) for d in measurement]
                values = [d['controlledproperty'] for d in measurement]
                ax.plot(dates, values, label=labels[i * group_size + j])
            ax.legend(loc='upper left', fontsize=font_size)
            ax.grid(True)
            ax.set_ylim(min_value, max_value)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y %H:%M'))
            ax.tick_params(axis='x', rotation=45, labelsize=font_size)
            ax.tick_params(axis='y', labelsize=font_size)
        return fig
