"""
Author: Kyle Koeller
Created: 4/13/2022
Last Updated: 4/13/2022
"""

import pandas as pd
import numpy as np


def main():
    """
    Calculates the Cousins R_c value for a given B, V, g', and r' from APASS

    :return: Outputs a file to be used for R_c values
    """
    # predefined values do not change
    alpha = 0.278
    e_alpha = 0.016
    beta = 1.321
    e_beta = 0.03
    gamma = 0.219

    # import file from Catalog Finder or Catalog Comparison
    input_file = input("Enter the text file name from Catalog Finder or Catalog Comparison: ")
    df = pd.read_csv(input_file, header=None, skiprows=[0], sep=",")

    # writes the columns from the input file
    ra = df[0]
    dec = df[1]
    B = df[2]
    e_B = df[3]
    V = df[4]
    e_V = df[5]
    g = df[6]
    e_g = df[7]
    r = df[8]
    e_r = df[9]

    Rc = []
    e_Rc = []
    count = 0
    # loop that goes through each value in B to get the total amount of values to be calculated
    for i in B:
        div = (alpha*(float(i) - float(V[count])) - gamma - float(g[count]) + float(r[count]))/beta
        val = float(V[count]) + div

        b_v = ((float(i) - float(V[count]))*e_alpha)**2
        v_rc = ((float(V[count]) - val)*e_beta)**2
        beta_alpha = ((beta - alpha)*float(e_V[count]))**2

        root = np.sqrt(b_v + v_rc + float(e_g[count])**2 + float(e_r[count])**2 + (alpha*float(e_B[count]))**2 + beta_alpha)
        # if the value is nan then append 99.999 to the R_c value and its error to make it obvious that there is no given value
        if isNaN(val) == True:
            Rc.append(99.999)
            e_Rc.append(99.999)
        else:
            Rc.append(format(val, ".2f"))
            e_Rc.append(format((1/beta)*root, ".2f"))
        count += 1

    # puts all columns into a dataframe for output
    final = pd.DataFrame({
        "RA": ra,
        "DEC": dec,
        "BMag": B,
        "e_BMag": e_B,
        "VMag": V,
        "e_VMag": e_V,
        "Rc": Rc,
        "e_Rc": e_Rc
    })

    # saves the dataframe to an entered output file
    output_file = input("Enter an output file name (i.e. 'APASS_254037_Rc_values.txt): ")
    final.to_csv(output_file, index=None, sep="\t")
    print("Finished Saving")


def isNaN(num):
    """
    Checks if a value is nan

    :param num: value to be checked
    :return: Boolean True or False
    """

    return num != num


if __name__ == '__main__':
    main()