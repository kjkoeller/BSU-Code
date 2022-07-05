# APASS Catalog Search
These programs allow the user to search the APASS catalog II/336/apass9 and compare the RA and DEC values with what comparison stars are found in Astro ImageJ (AIJ). In order to use these programs you NEED to download all three ".py" programs. To get the file output file of the comparison stars most likely in the same field as AIJ then all you need to run is the first program listed below.

The purpose of these three programs to GAIA band passes that generally considered to be more reliable than Tycho band passes most likely found on Simbad.

## APASS_AIJ_comparison_selector.py
The main program that runs this main folder. With this program you call upon the cousins_r.py and APASS_catalog_finder.py programs to compile a list of stars that are close to what AIJ found off Simbad and output a file that gives RA, DEC, B, V, R_c, and the respective band pass errors.

## cousins_r.py
From the paper listed in the program (https://arxiv.org/pdf/astro-ph/0609736.pdf) this program finds the Cousins R value from the band passes found in the APASS_catalog_finder and gives this output file to the APASS_AIJ_comparison_selector program.

## APASS_catalog_finder.py
Given an RA and DEC from simbad, finds stars 40 arc min box around those qoordinates from the APASS catalog. This program then outputs these stars and numerous band passes to a text file that will be saved and used by the cousins_r.py program.
