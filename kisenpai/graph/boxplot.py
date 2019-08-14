"""
1. Boxplot

A box and whisker plot—also called a box plot—displays the five-number summary of a set of data.
The five-number summary is the
- minimum,
- first quartile,
- median,
- third quartile,
- and maximum.

In a box plot, we draw a box from the first quartile to the third quartile.
A vertical line goes through the box at the median. The whiskers go from each
quartile to the minimum or maximum.

                Q1   median    Q2
min             |-------------|               max
o---------------|      |      |---------------o
                |-------------|

data : list, tuple, numpy.ndarray, pd.series.Series
notch : Boolean # If True, will produce a notched box plot.
graph_orientation : string # If 'h' (default), makes the boxes horizontally . If 'v', everything is drawn vertical.
show_outliers : Boolean # if True (default) Show the outliers beyond the caps.
hide_box : Boolean # if False (default) 

"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Boxplot:

    def __init__(self, data, notched_box=False, graph_orientation='h',
                 show_outliers=True,title='Box plot'):
        if not isinstance(data, (list, pd.core.series.Series, np.ndarray, tuple)):
            raise Exception('wrong type')

        self.data = data
        self.notched_box = notched_box
        self.graph_orientation = graph_orientation
        self.show_outliers = show_outliers
        self.title = title

    def show(self):
        if self.data is None:
            raise Exception('Please insert data')

        vert = True
        if self.graph_orientation == 'h' or self.graph_orientation == 'horizontal':
            vert = False

        plt.boxplot(x=self.data, vert=vert, showfliers=self.show_outliers, showbox=False)
        plt.show()
