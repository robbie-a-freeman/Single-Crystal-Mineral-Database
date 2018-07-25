"""Contains helper functions for loading the database.
"""

import pandas as pd

#import changelog
#import allEntries
import tableManager

__author__ = "Robbie Freeman"
__credits__ = ["Thomas Duffy"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

# Grab the CSV file in the database, skip the the header line assuming it's still
# the fourth line in the sheet.
def getInitialTable():
    # Could add converters={'col'=to_numeric} to hold int/float values for numbers
    # in the dataframe
    table = pd.read_csv("static/downloads/single-crystal_db.csv", header=4, skip_blank_lines=True, skipinitialspace=True)

    # Get rid of all lines with all NaN values (not including class labels)
    table.dropna(inplace=True, how="all", axis=1) # columns
    table.dropna(inplace=True, how="all", axis=0) # rows
    return table
