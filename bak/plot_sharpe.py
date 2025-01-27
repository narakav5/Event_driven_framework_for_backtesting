# -*- coding: utf-8 -*-

# plot_sharpe.py

import matplotlib.pyplot as plt
import numpy as np


def create_data_matrix(csv_ref, col_index):
    data = np.zeros((3, 3))
    for i in range(0, 3):
        for j in range(0, 3):
            data[i][j] = float(csv_ref[i * 3 + j][col_index])
    return data


if __name__ == "__main__":
    csv_file = open("opt.csv", "r").readlines()
    csv_ref = [
        c.strip().split(',')
        for c in csv_file if c[:3] == "100"
    ]
    print(csv_ref)
    data = create_data_matrix(csv_ref, 4)
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(data, cmap=plt.cm.Blues)
    row_labels = [0.5, 1.0, 1.5]
    column_labels = [2.0, 3.0, 4.0]
    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            plt.text(x + 0.5, y + 0.5, '%.2f%%' % data[y, x],
                     horizontalalignment='center',
                     verticalalignment='center')
    plt.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.set_xticklabels(row_labels, minor=False)
    ax.set_yticklabels(column_labels, minor=False)

    plt.suptitle('Sharpe Ratio HeatMap', fontsize=18)
    plt.xlabel('Z-score Exit Threshold', fontsize=14)
    plt.ylabel('Z-score Entry Threshold', fontsize=14)
    plt.show()
