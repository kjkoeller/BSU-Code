"""
Author: Kyle Koeller
Date Created: 03/04/2022
Last Updated: 4/20/2022

This program fits a set of data with numerous polynomial fits of varying degrees
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial
import statsmodels.formula.api as smf
import os
import seaborn as sns


def data_fit():
    """
    Create a linear fit by hand and than use scipy to create a polynomial fit given an equation along with their
    respective residual plots.

    :return: Fits and residuals for a given data set
    """
    # read in the text file
    isFile = None
    while not isFile:
        # make sure the input_file is a real file
        input_file = input("Either enter the file name if the file is in the same folder as the program or the file "
                           "path: ")
        isFile = os.path.isfile(input_file)
        if isFile:
            break
        else:
            print("The file/file-path does not exist, please try again.")
            print()

    # noinspection PyUnboundLocalVariable
    df = pd.read_csv("total_minimums.txt", header=None, delim_whitespace=True)

    # append values to their respective lists for further and future potential use
    x = df[1]
    y = df[2]
    y_err = df[3]

    x1 = []
    y1 = []
    y_err_new = []
    count = 0
    # collects only primary times of minima and its corresponding O-C and O-C error
    for i in x:
        if i.is_integer():
            x1.append(i)
            y1.append(y[count])
            y_err_new.append(y_err[count])
        count += 1

    x1 = np.array(x1)
    y1 = np.array(y1)

    # noinspection PyArgumentList
    xs = np.linspace(x.min(), x.max(), 1000)

    # numpy curve fit
    degree_test = None
    while not degree_test:
        # make sure the value entered is actually an integer
        try:
            degree = int(input("How many polynomial degrees do you want to fit (integer values > 0): "))
            degree_test = True
        except ValueError:
            print("This is not an integer, please enter an integer.")
            print()
            degree_test = False

    print("")
    line_style = [(0, (1, 10)), (0, (1, 1)), (0, (5, 10)), (0, (5, 5)), (0, (5, 1)),
                  (0, (3, 10, 1, 10)), (0, (3, 5, 1, 5)), (0, (3, 1, 1, 1)), (0, (3, 5, 1, 5, 1, 5)),
                  (0, (3, 10, 1, 10, 1, 10)), (0, (3, 1, 1, 1, 1, 1))]
    line_count = 0
    i_string = ""

    # beginning latex to a latex table
    beginningtex = """\\documentclass{report}
            \\usepackage{booktabs}
            \\begin{document}"""
    endtex = "\end{document}"

    # opens a file with this name to begin writing to the file
    output_test = None
    while not output_test:
        output_file = input("What is the output file name for the regression tables (either .txt or .tex): ")
        if output_file.endswith((".txt", ".tex")):
            output_test = True
        else:
            print("This is not an allowed file output. Please make sure the file has the extension .txt or .tex.")
            print()

    # noinspection PyUnboundLocalVariable
    f = open(output_file, 'w')
    f.write(beginningtex)

    # noinspection PyUnboundLocalVariable
    for i in range(1, degree + 1):
        """
        Inside the model variable:
        'np.polynomial.polynomial.polyfit(x, y, i)' gathers the coefficients of the line fit
        
        'Polynomial' then finds an array of y values given a set of x data
        """
        model = Polynomial(np.polynomial.polynomial.polyfit(x1, y1, i))
        # if you want to look at the more manual way of finding the R^2 value un-comment the following line otherwise
        # stick with the current regression table print("Polynomial of degree " + str(i) + " " + str(adjR(x, y, i)))
        # print("")

        # plot the main graph with both fits (linear and poly) onto the same graph
        plt.plot(xs, model(xs), color="black", label="polynomial fit of degree " + str(i),
                 linestyle=line_style[line_count])
        line_count += 1

        # this if statement adds a string together to be used in the regression analysis
        # pretty much however many degrees in the polynomial there are, there will be that many I values
        if i >= 2:
            i_string = i_string + " + I(x**" + str(i) + ")"
            mod = smf.ols(formula='y ~ x' + i_string, data=df)
            res = mod.fit()
            f.write(res.summary().as_latex())
        elif i == 1:
            mod = smf.ols(formula='y ~ x', data=df)
            res = mod.fit()
            f.write(res.summary().as_latex())

    f.write(endtex)
    # writes to the file the end latex code and then saves the file
    f.close()
    print("Finished saving latex/text file.")

    plt.errorbar(x1, y1, yerr=y_err, fmt="o", color="black")
    # make the legend always be in the upper right hand corner of the graph
    plt.legend(loc="upper right")

    empty = None
    while not empty:
        x_label = input("X-Label: ")
        y_label = input("Y-Label: ")
        title = input("Title: ")
        if not x_label:
            print("x label is empty. Please enter a string or value for these variables.")
            print()
        elif not y_label:
            print("y label is empty. Please enter a string or value for these variables.")
            print()
        else:
            empty = True

    # noinspection PyUnboundLocalVariable
    plt.xlabel(x_label)
    # noinspection PyUnboundLocalVariable
    plt.ylabel(y_label)
    # noinspection PyUnboundLocalVariable
    plt.title(title)
    plt.grid()
    plt.show()

    # noinspection PyUnboundLocalVariable
    residuals(x1, y1, x_label, y_label, degree, model, xs)


def residuals(x, y, x_label, y_label, degree, model, xs):
    """
    This plots the residuals of the data from the input file
    :param x: original x data
    :param y: original y data
    :param x_label: x-axis label
    :param y_label: y-axis label
    :param degree: degree of the polynomial fit
    :param model: the last model (equation) that was used from above
    :param xs: numpy x data set
    :return: none
    """
    # appends the y values from the model to a variable
    y_model = model(xs)

    # makes dataframes for both the raw data and the model data
    raw_dat = pd.DataFrame({
        x_label: x,
        y_label: y,
    })

    model_dat = pd.DataFrame({
        x_label: xs,
        y_label: y_model
    })

    # allows for easy change of the format of the subplots
    rows = 2
    cols = 1
    # creates the figure subplot for appending next
    axs = plt.subplots(rows, cols, figsize=(9, 5))
    # adds gridlines to both subplots
    axs[0].grid(visible=True, which='major', color='black', linewidth=1.0)
    axs[0].grid(visible=True, which='minor', color='black', linewidth=0.5)
    axs[1].grid(visible=True, which='major', color='black', linewidth=1.0)
    axs[1].grid(visible=True, which='minor', color='black', linewidth=0.5)

    # creates the model line fit
    sns.lineplot(x=x_label, y=y_label, data=model_dat, ax=axs[0], color="red")
    # plots the original data to the same subplot as the model fit
    # edge color is removed to any sort of weird visual overlay on the plots as the normal edge color is white
    sns.scatterplot(x=x_label, y=y_label, data=raw_dat, ax=axs[0], color="black", edgecolor="none")
    # plots the residuals from the original data to the polynomial degree from  above
    sns.residplot(x=x_label, y=y_label, order=degree, data=raw_dat, ax=axs[1], color="black",
                  scatter_kws=dict(edgecolor="none"))
    # adds a horizontal line to the residual plot to represent the model line fit with the same color
    axs[1].axhline(y=0, color="red")

    plt.show()


def adjR(x, y, degree):
    """
    Finds the R Squared value for a given polynomial degree manually

    :param x: x data points
    :param y: y data points
    :param degree: polynomial degree

    :return: R squared value
    """

    results = {}
    coeffs = np.polyfit(x, y, degree)
    p = np.poly1d(coeffs)
    yhat = p(x)
    ybar = np.sum(y) / len(y)
    ssreg = np.sum((yhat - ybar) ** 2)
    sstot = np.sum((y - ybar) ** 2)
    results["r_squared"] = 1 - (((1 - (ssreg / sstot)) * (len(y) - 1)) / (len(y) - degree - 1))

    return results


if __name__ == '__main__':
    data_fit()
