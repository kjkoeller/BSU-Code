"""
Author: Kyle Koeller
Date Created: 03/04/2022

This program fits a set of data with numerous polynomial fits of varying degrees
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial
import statsmodels.formula.api as smf
import os


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
    f = open(file_name, 'w')
    f.write(beginningtex)
    
    # noinspection PyUnboundLocalVariable
    for i in range(1, degree+1):
        """
        Inside the model variable:
        'np.polynomial.polynomial.polyfit(x, y, i)' gathers the coefficients of the line fit
        
        'Polynomial' then finds an array of y values given a set of x data
        """
        model = np.poly1d(np.polyfit(x_new, y, i))
        # if you want to look at the more manual way of finding the R^2 value un-comment the following line otherwise
        # stick with the current regression table print("Polynomial of degree " + str(i) + " " + str(adjR(x, y, i)))
        # print("")
        
        # plot the main graph with both fits (linear and poly) onto the same graph
        plt.plot(xs, model(xs), color="black", label="polynomial fit of degree " + str(i), linestyle=line_style[line_count])
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
    
    # noinspection PyUnboundLocalVariable
    # print(res.summary())
    
    f.write(endtex)
    # writes to the file the end latex code and then saves the file
    f.close()
    print("Finished saving latex/text file.")
    
    plt.errorbar(x, y, yerr=y_err, fmt="o", color="black")
    # make the legend always be in the upper right hand corner of the graph
    plt.legend(loc="upper right")
    plt.xlabel(input("X-Label: "))
    plt.ylabel(input("Y-Label: "))
    plt.title(input("Title: "))
    plt.grid()
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
    ybar = np.sum(y)/len(y)
    ssreg = np.sum((yhat-ybar)**2)
    sstot = np.sum((y - ybar)**2)
    results["r_squared"] = 1 - (((1-(ssreg/sstot))*(len(y)-1))/(len(y)-degree-1))

    return results


if __name__ == '__main__':
    data_fit()
