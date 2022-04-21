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

    final = aij.angle_dist(df, dh)

    # prints the output and saves the dataframe to the text file with "tab" spacing
    output_file = input("Enter an output file name (i.e. 'APASS_254037_Catalog.txt): ")
    final.to_csv(output_file, index=None, sep="\t")
    print("Finished Saving")


if __name__ == '__main__':
    main()
