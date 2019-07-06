"""Generates all entries in the database in a specific format that is easier to
   browse in bulk and a lot quicker than in fetch.py. Using pandas, loads the
   master sheet, cleans it up, and adds backslashes before shipping it to the
   html template. The backslashes are necessary to be parsed in javascript.
   Outputs the text into a file.
"""

import pandas as pd
import math
import sys
import os
import xlrd

import tableManager

__author__ = "Robbie Freeman"
__credits__ = ["Thomas Duffy"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

# Reads in the master sheet with the DB info and return a formatted string for
# use in the js file entries.js
def main():
    # Read in the DB, specifically just the nominal columns of each publicly
    # accessible sheet.
    table = tableManager.getInitialTableQuick()

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
        editedTable += str(names[i]) + "~*" + str(compositions[i]) + "~*" + str(groups[i]) + "~*" + str(i) + "~*" + str(lineBreaks[i])

    # save the table in a .txt file
    if os.path.isfile('static/text/all.txt'):
        os.remove("static/text/all.txt")

    # remove the last backslash so that the file terminates and return the table.
    editedTable = editedTable[:-1]
    orig_stdout = sys.stdout
    file = open('static/text/all.txt', 'w')
    sys.stdout = file
    print(editedTable.encode("utf-8"), end='')
    sys.stdout = orig_stdout
    file.close()
