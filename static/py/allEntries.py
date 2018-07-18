"""Generates all entries in the database in a specific format that is easier to
   browse in bulk and a lot quicker than in fetch.py. Using pandas, loads the
   master sheet, cleans it up, and adds backslashes before shipping it to the
   html template. The backslashes are necessary to be parsed in javascript.
"""

import pandas as pd
import math

__author__ = "Robbie Freeman"
__credits__ = ["Thomas Duffy"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

# Reads in the master sheet with the DB info and return a formatted string for
# use in the js file entries.js
def main():
    # Read in the DB
    table = pd.read_csv("static/downloads/single-crystal_db.csv", usecols=[0, 1, 2], header=4, skip_blank_lines=True, skipinitialspace=True)

    # Get rid of all lines with NaN values
    table.dropna(inplace=True, how="all", axis=1)
    table.dropna(inplace=True, how="all", axis=0)
    table.dropna(inplace=True, how="any", axis=0)
    print(table)

    # insert the backslash for new line in js
    # also extra two backslashes to allow js to split the string
    table.insert(3, "\\\\\\", "\\\\\\")

    # format the table into a string that is easy to read in via js
    # collect the data and check it
    names = table["Name"].tolist()
    compositions = table["Composition"].tolist()
    groups = table["Group"].tolist()
    lineBreaks = table["\\\\\\"].tolist()

    assert (len(names) == len(compositions) == len(groups) == len(lineBreaks))

    # build the string row-by-row
    editedTable = ""
    for i in range(len(names)):
        editedTable += names[i] + "~*" + compositions[i] + "~*" + groups[i] + "~*" + lineBreaks[i]

    # remove the last backslash so that the file terminates and return the table
    editedTable = editedTable[:-1]
    return editedTable
