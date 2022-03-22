"""
Author: Kyle Koeller
Date Created: 03/04/2022

This program fits a set of data with numerous polynomial fits of varying degrees
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def data_fit():
    """
    Create a linear fit by hand and than use scipy to create a polynomial fit given an equation along with their
    respective residual plots.

    :return: Fits and residuals for a given data set
    """

    # read in the text file
    df = pd.read_csv("total_minimums.txt", header=None, delim_whitespace=True)

    x = df[1]
    y = df[2]
    y_err = df[3]
    N = len(x)

    x_new = []
    for i in x:
        print(type(i), i)
        if type(i) == int:
            x_new.append(i)

    x_new = pd.DataFrame(x_new)
    print(x_new)
    xs = np.linspace(x_new.min(), x_new.max(), 1000)

    # numpy curve fit
    degree = 5
    line_style = [(0, (1, 10)), (0, (1, 1)), (0, (5, 10)), (0, (5, 5)), (0, (5, 1)),
                  (0, (3, 10, 1, 10)), (0, (3, 5, 1, 5)), (0, (3, 1, 1, 1)), (0, (3, 5, 1, 5, 1, 5)),
                  (0, (3, 10, 1, 10, 1, 10)), (0, (3, 1, 1, 1, 1, 1))]
    line_count = 0
    for i in range(1, degree+1):
        model = np.poly1d(np.polyfit(x_new, y, i))
        print("Polynomial of degree " + str(i) + " R^2: "+str(adjR(x, y, i)))
        print("")

        # plot the main graph with both fits (linear and poly) onto the same graph
        plt.plot(xs, model(xs), color="black", label="polynomial fit of degree " + str(i), linestyle=line_style[line_count])
        line_count += 1

    plt.errorbar(x, y, yerr=y_err, fmt="o", color="black")
    # make the legend always be in the upper right hand corner of the graph
    plt.legend(loc="upper right")
    plt.xlabel("Epoch Number")
    plt.ylabel("O-C (days)")
    plt.title("NSVS 254037 O-C")
    plt.grid()
    plt.show()


def adjR(x, y, degree):
    """
    Finds the R Squared value for a given polynomial degree

    :param x: x data points
    :param y: y data points
    :param degree: polynomial degree
    :return: R squared value
    """
    results = {}
    coeffs = np.polyfit(x, y, degree)
    p = np.poly1d(coeffs)
    yhat = p(x)
    ybar = np.sum(y)/len(y)
    ssreg = np.sum((yhat-ybar)**2)
    sstot = np.sum((y - ybar)**2)
    results["r_squared"] = 1 - (((1-(ssreg/sstot))*(len(y)-1))/(len(y)-degree-1))

    return results


if __name__ == '__main__':
    data_fit()
