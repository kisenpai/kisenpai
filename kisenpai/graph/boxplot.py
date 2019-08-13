import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# agg backend is used to create plot as a .png file
# mpl.use('agg')


class Boxplot:

    def __init__(self, data, graph_orientation='horizontal', title='Box plot'):
        self.data = data
        self.graph_orientation = graph_orientation
        self.title = title

    def show(self):
        if self.data is None:
            raise Exception('Please insert data')

        if self.graph_orientation == 'v' or self.graph_orientation == 'vertical':
            vert = True
        else:
            vert = False

        print('graph_orientation', vert)

        plt.boxplot(self.data, vert)
        plt.show()
