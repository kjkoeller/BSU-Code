# BSU-Code
Projects currently working on at Ball State University for the Physics and Astronomy Department for my Masters Thesis

# AIJ Filter Collection
This program is meant to make the process of collecting the different filters from AIJ excel spreadsheets faster.
The user enters however many nights they have and the program goes through and checks those text files for the
different columns for, HJD, Amag, and Amag error for the B, V, R filters.

# APASS Catalog Search
First run APASS_catalog_comparison_finder to search through the APASS catalog around the field of the user's system. This will produce a text file with hundreds of potential stars in the field and this allows the user to then compare these RA and DEC to what AIJ produced with its .RADEC file type. Once both AIJ and the first code have been run, the user can then run APASS_AIJ_comparison_selector to compare the two files to produce a file that gives RA, DEC, B mag (err), and V mag (err). The whole purpose is to use APASS magnitudes within AIJ to generate higher quality photometry analysis.

# TESS Database Search
Allows a user to search through the TESS database and save light curve files as CSV's to the local machine. Also allows the user to do period analysis on each data set that TESS has.
