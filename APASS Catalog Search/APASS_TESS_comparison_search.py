"""
Author: Kyle Koeller
Created: 2/8/2022
Last Updated: 4/21/2022
Python Version 3.X

APASS Star comparison finding for the most accurate magnitudes from the list of stars made in AIJ
"""

from __future__ import print_function, division
import pandas as pd
import APASS_AIJ_comparison_selector as aij


def main():
    # reads the text files to be analyzed for comparison star matches between APASS and Simbad
    apass_file = input("Enter the text file name for the generated APASS stars: ")
    print()
    print("You must delete all rows in the RA and DEC file from AIJ that do not have numbers (i.e. Delete the first 10 lines or so)")
    radec_file = input("Enter the text file name for the RADEC file from AIJ: ")
    df = pd.read_csv(apass_file, header=None, skiprows=[0], sep=",")
    dh = pd.read_csv(radec_file, header=None)

    final = aij.angle_dist(apass_file, radec_file)

    # prints the output and saves the dataframe to the text file with "tab" spacing
    output_file = input("Enter an output file name (i.e. 'APASS_254037_Catalog.txt): ")
    final.to_csv(output_file, index=None, sep="\t")
    print("Finished Saving")


def splitter(a):
    """
    Splits the truncated colon RA and DEC from simbad into decimal forms

    :param a:
    :return:
    """
    # makes the coordinate string into a decimal number from the text file
    step = []
    final = []
    for i in a:
        new = i.split(":")
        num1 = int(new[0])
        num2 = int(new[1])
        num3 = int(float(new[2]))
        b = num1 + ((num2 + (num3/60))/60)
        step.append(format(b, ".7f"))

    for i in step:
        final.append(float(format(i)))

    return final


def new_list(a):
    """
    Converts lists into number format with minimal decimal places

    :param a: list
    :return: new list with floats
    """
    b = []
    for i in a:
        b.append(float(format(i, ".2f")))
    return b


def conversion(a):
    """
    Converts decimal RA and DEC to standard output with colons

    :param a: decimal RA or DEC
    :return: truncated version using colons
    """
    b = []
    print(a)
    for i in a:
        num1 = float(i)
        num2 = (num1 - int(num1)) * 60
        num3 = format((num2 - int(num2)) * 60, ".3f")
        b.append(str(int(num1)) + ":" + str(int(num2)) + ":" + str(num3))
    return b


if __name__ == '__main__':
    main()
