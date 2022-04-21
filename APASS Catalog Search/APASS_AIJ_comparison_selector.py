"""
Author: Kyle Koeller
Created: 2/8/2022
Last Updated: 4/21/2022
Python Version 3.X

APASS Star comparison finding for the most accurate magnitudes from the list of stars made in AIJ
"""

from __future__ import print_function, division
import pandas as pd
from PyAstronomy import pyasl
import APASS_catalog_finder as APASS_catalog


def main():
    # reads the text files to be analyzed for comparison star matches between APASS and Simbad
    apass_file = input("Enter the text file name for the generated APASS stars: ")
    radec_file = input("Enter the text file name for the RADEC file from AIJ: ")
    while True:
        test = 0
        try:
            df = pd.read_csv(apass_file, header=None, skiprows=[0], sep="\t")
            dh = pd.read_csv(radec_file, header=None)
        except FileNotFoundError:
            print("Files were not found, please enter them again.")
            print()
            test = -1
        if test == 0:
            break
        else:
            apass_file = input("Enter the text file name for the generated APASS stars: ")
            radec_file = input("Enter the text file name for the RADEC file from AIJ: ")
    
    # noinspection PyUnboundLocalVariable
    duplicate_df = angle_dist(df, dh)

    # prints the output and saves the dataframe to the text file with "tab" spacing
    output_file = input("Enter an output file name (i.e. 'APASS_254037_Catalog.txt): ")
    duplicate_df.to_csv(output_file, index=None, sep="\t")
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
        b = num1 + ((num2 + (num3 / 60)) / 60)
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
    for i in a:
        num1 = float(i)
        num2 = (num1 - int(num1)) * 60
        num3 = format((num2 - int(num2)) * 60, ".3f")
        b.append(str(int(num1)) + ":" + str(int(num2)) + ":" + str(num3))
    return b


def angle_dist(df, dh):
    """
    Gathers a list of stars that are very close to the ones given in the RADEC file
    
    :param df: apass dataframe
    :param dh: radec dataframe
    :return: compared list
    """
    # checks specific columns and adds those values to a list variable for comparison in the nested for loops below
    apass_dec = list(df[1])
    apass_ra = list(df[0])
    simbad_dec = list(dh[1])
    simbad_ra = list(dh[0])

    # converts the RA and Dec coordinate format to decimal format
    apass_split_ra = APASS_catalog.splitter(apass_ra)
    apass_split_dec = APASS_catalog.splitter(apass_dec)

    simbad_split_ra = APASS_catalog.splitter(simbad_ra)
    simbad_split_dec = APASS_catalog.splitter(simbad_dec)

    comp = pd.DataFrame()
    simbad_count = 0
    # finds the comparison star in both APASS text file and RA and Dec files to an output variable with
    # the RA and Dec noted for magnitude finding
    for i in simbad_split_dec:
        apass_count = 0
        for k in apass_split_dec:
            radial = pyasl.getAngDist(float(apass_split_ra[apass_count]), float(k),
                                      float(simbad_split_ra[simbad_count]),
                                      float(i))
            if radial <= 0.025:
                comp = comp.append(df.loc[apass_count:apass_count], ignore_index=True)
            apass_count += 1
        simbad_count += 1

    # removes all duplicate rows from the dataframe
    duplicate_df = comp.drop_duplicates()

    try:
        ra_final = list(duplicate_df[0])
    except KeyError:
        print("There were no comparison stars found between the two text files.")
        exit()

    return duplicate_df


if __name__ == '__main__':
    main()
