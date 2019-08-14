import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from kisenpai.graph.boxplot import Boxplot


def main():
    spread = np.random.rand(50) * 100
    center = np.ones(25) * 50
    flier_high = np.random.rand(10) * 100 + 100
    flier_low = np.random.rand(10) * -100
    data = np.concatenate((spread, center, flier_high, flier_low), 0)
    print(data)

    tips = sns.load_dataset("tips")
    # print(tips.info())
    # print(tips['total_bill'])

    bp_total_bill = Boxplot(data=data, graph_orientation='v')

    bp_total_bill.show()


if __name__ == '__main__':
    main()
