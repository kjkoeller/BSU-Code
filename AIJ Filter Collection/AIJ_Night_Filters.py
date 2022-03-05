"""
Created: November 11, 2020
Author: Kyle Koeller
Python Version 3.9

This program is meant to make the process of collecting the different filters from AIJ excel spreadsheets faster.
The user enters however many nights they have and the program goes through and checks those text files for the
different columns for,HJD, Amag, and Amag error for the B and V filters.

The program will also calculate the R magnitude from the rel flux of T1.

There are error catching statements within the program so if the user mistypes, the program will not crash and
close on them.
"""

import pandas as pd
import math as mt
from os import path


def main(c):
    # warning prompts for the user to read to make sure this program works correctly
    if c == 0:
        # warning prompts for the user to read to make sure this program works correctly
        print()
        print("Make sure you have turned the output xls files from AIJ into tab delimited text files. "
              "Since these xls files are corrupt for reading directly from.")
        print("You will also need to go into each night and filter and "
              "make the HJD column 6 decimals instead of the output of 3 within Excel.")
        print()
    else:
        print()

    while True:
        # checks to see whether you have entered a number and a correct filter letter
        try:
            num = int(input("Number of nights you have: "))
            filter_name = input("Which filter are these nights in (B, V, R): ")
            if filter_name.upper() == "B" or filter_name.upper() == "V" or filter_name.upper() == "R":
                break
            else:
                print("Please enter B, V, or R for your filter.")
                print()
                continue
        except ValueError:
            print("You have entered an invalid number for your number of nights. Please enter a number.")
            print("")

    get_filters(num, filter_name)


def get_filters(n, f):
    """
    Takes a number of nights for a given filter and takes out the HJD, either A_Mag1 or T1_flux, and
    error for mag or flux

    :param n: Number of observation nights
    :param f: The filter letter being used
    :return: the output text files for each night in a given filter
    """
    total_hjd = []
    total_amag = []
    total_error = []
    total_flux = []
    # checks for either the b, v, r filter as either upper or lowercase will work
    if f.lower() == "b" or f.lower() == "v":
        for i in range(n):
            while True:
                # makes sure the file pathway is real and points to some file
                # (does not check if that file is the correct one though)
                try:
                    # an example pathway for the files
                    # E:\Research\Data\NSVS_254037\2018.10.12-reduced\Check\V\2018.10.12.APASS.V_measurements.txt
                    file = input("Enter night %d file path: " % (i+1))
                    if path.exists(file):
                        break
                    else:
                        continue
                except FileNotFoundError:
                    print("Please enter a correct file path")

            # noinspection PyUnboundLocalVariable
            df = pd.read_csv(file, delimiter="\t")

            # set parameters to lists from the file by the column header
            hjd = []
            amag = []
            amag_error = []
            try:
                hjd = list(df["HJD"])
                amag = list(df["Source_AMag_T1"])
                amag_error = list(df["Source_AMag_Err_T1"])
            except KeyError:
                print("The file you entered does not have the columns of HJD, Source_AMag_T1, or Source_AMag_Err_T1. "
                      "Please re-enter the file path and make sure its the correct file.")
                c = 1
                main(c)

            total_hjd.append(hjd)
            total_amag.append(amag)
            total_error.append(amag_error)

        # converts the Dataframe embedded lists into a normal flat list
        new_hjd = [item for elem in total_hjd for item in elem]
        new_amag = [item for elem in total_amag for item in elem]
        new_error = [item for elem in total_error for item in elem]

        # outputs the new file to dataframe and then into a text file for use in Peranso or PHOEBE
        data = pd.DataFrame({
            "HJD": new_hjd,
            "AMag": new_amag,
            "AMag Error": new_error
        })
        print("")
        output = input("What is the file output name (with file extension .txt): ")

        data.to_csv(output, index=False, header=False, sep='\t')
        print("")
        print("Fished saving the file to the same location as this program.")

    # same process as the b or v filter except it checks for the rel flux of T1 instead of the AMag
    elif f.lower() == "r":
        for i in range(n):
            while True:
                try:
                    # E:\Research\Data\NSVS_254037\2018.09.18-reduced\Check\R\2018.09.18.APASS.R_measurements.txt
                    file = input("Enter night " + str(i + 1) + " file path: ")
                    break
                except FileNotFoundError:
                    print("Please enter a correct file path")
            # noinspection PyUnboundLocalVariable
            df = pd.read_csv(file, delimiter="\t")

            hjd = []
            flux = []
            try:
                hjd = list(df["HJD"])
                flux = list(df["rel_flux_T1"])
            except KeyError:
                print("The file you entered does not have the columns of HJD or rel_flux_T1. "
                      "Please re-enter the file path and make sure its the correct file.")
                c = 1
                main(c)

            total_hjd.append(hjd)
            total_flux.append(flux)

        # converts the Dataframe embedded lists into a normal flat list
        new_hjd = [item for elem in total_hjd for item in elem]
        new_flux = [item for elem in total_flux for item in elem]

        counter = 0
        new_error = []
        while counter != len(new_flux):
            new_error.append(0.01)
            counter += 1

        update_flux = []
        for i in new_flux:
            u_flux = (-2.5) * (mt.log10(i))
            update_flux.append(format(u_flux, '.6f'))

        data = pd.DataFrame({
            "HJD": new_hjd,
            "Flux": update_flux,
            "Flux Error": new_error
        })
        print("")
        output = input("What is the file output name (with file extension .txt): ")

        data.to_csv(output, index=False, header=False, sep='\t')
        print("")
        print("Fished saving the file to the same location as this program.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    count = 0
    main(count)
