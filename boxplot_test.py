import seaborn as sns
import matplotlib.pyplot as plt

from kisenpai.graph.boxplot import Boxplot


def main():
    tips = sns.load_dataset("tips")
    # print(tips.info())
    print(tips['total_bill'])
    sns.boxplot(x=tips['total_bill'])

    bp_total_bill = Boxplot(data=tips['total_bill'], graph_orientation='vertical')
    print(bp_total_bill.graph_orientation)

    bp_total_bill.show()


if __name__ == '__main__':
    main()
