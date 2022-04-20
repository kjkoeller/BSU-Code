"""
Look up the TESS data and download that data onto a local drive in the form of CSV files.

Author: Kyle Koeller
Date: February 19, 2022
Version: Python 3.9

This program is meant to make the process of collecting the different filters from AIJ excel spreadsheets faster.
The user enters however many nights they have and the program goes through and checks those text files for the
different columns for, HJD, Amag, and Amag error for the B, V, and R filters.
"""
# import required packages
import lightkurve as lk
import matplotlib.pyplot as plt


def main():
    """
    This 'list' variable searches through the TESS data to find light-curves that correspond to the name in the
    parentheses. The target name is under the TIC tag instead of NSVS, GAIA, TYC, or 2MASS.
    You can speicify a specific list number using this as an example 'list = lk.search_lightcurve("NSVS 896797")[2]'
    """
    # 'system' and 'search' name are meant to be separate one for searching TESS (search) and one for file name (system)
    system_name = input("Enter in a name of a system but replace all spaces with '_' (underscores) ex:NSVS_896797: ")
    search_name = system_name.replace("_", " ")
    li = lk.search_lightcurve(search_name)
    print(li)
    '''
    The for loop searches loops through the total number of items in the list and exports the data to csv files.
    to distinguish between the differing files use the '%d' notation where you want different numbers.
    i.e. 'tess%d_data.csv' will place a number for each iteration of the for loop and export tess0data.csv, tess1data.csv...
    Also, leave the 'r' in-front of the file path as you will otherwise produce an error.
    '''
    for i in range(0, len(li.table.columns["#"])):
        lc = li[i].download()
        """
        Exports the light curve file to a CSV
        Leave on True or you will receive an error warning that the file already exists if you run this more than
        once.
        """
        lc.to_csv(r"C:\Users\Kyle\OneDrive\PhysicsAstro\Astronomy\Code\Tess_Search\%s_tess%d_data.csv" % (system_name, i),
                  overwrite=True)
        # remove column with NaNs in them, and removes data points that are X sigma times the Standard deviation
        lc = lc.remove_nans().remove_outliers(sigma=3.0)
        print("Saved dataset %d" % i)
        # plot the unfolded raw light curve (not that useful without folding the light curve with the period
        # lc.plot()
        # allows the user to fold a region selected period over the light curve
        period_analysis(lc)
    print("Finished saving all files.")


def period_analysis(lc):
    """
    Produces a period that is half of what it should be. This first period analysis is less accurate than the following
    due to the lower precision but is still needed as a guide for the following procedure (so leave in).

    :param lc:
    :return: nothing
    """
    pg = lc.normalize(unit='ppm').to_periodogram()
    # period = pg.period_at_max_power
    '''
    You will need to update the minmum_period and maximum_period to what your specific system has. The example below
    are the periods of NSVS 896797 with what the TESS data was producing for me. You do not need to get this specific,
    most likely 4 decimal places will suffice.
    
    This next section is the much more accurate period search, as this allows you to systematically search in a range
    that you set. Rather than just a blanket maximum frequency.
    '''
    print()
    decision = False
    minimum = 0.25
    maximum = 1.25
    print("You must close the previous graphs in order to move along with the next prompts.")
    print()
    while not decision:
        try:
            pg = lc.to_periodogram(minimum_period=minimum, maximum_period=maximum, oversample_factor=10000)
            new_period = pg.period_at_max_power
            lc.fold(new_period).scatter(label=rf'New_Period = {new_period.value:.6f} d')
            # prints new period for future records.
            print(new_period)
            pg.plot(view='period')
            plt.show()
        except ValueError:
            print()
            print("Cannot enter a negative value for periods.")
            print()
            # user_input = input("Do you want to do another range adjustment (Yes or No): ")
        user_input = input("Do you want to do another range adjustment (Yes or No): ")
        ui = False
        while not ui:
            if user_input.lower() == "yes":
                minimum = float(input("Please enter a minimum period value you would like to look at: "))
                maximum = float(input("Please enter a maximum period value you would like to look at: "))
                ui = True
            elif user_input.lower() == "no":
                # noinspection PyUnboundLocalVariable
                print("Found period: %.9f" % new_period.value)
                print("")
                decision = True
                ui = True
            else:
                print("Must enter 'Yes' or 'No' exlcusively.")
                user_input = input("Do you want to do another range adjustment (Yes or No): ")


if __name__ == '__main__':
    main()
    # Citation purposes for papers and such
    # lk.show_citation_instructions()
