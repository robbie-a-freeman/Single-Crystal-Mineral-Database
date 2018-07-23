"""Script that checks for changes uploaded to the database by Tom through
FileZilla and updates the master sheet to be the new sheet. Then, it alters the
changelog.html file to reflect the changes. Uses pandas for the table changes
and Beautiful Soup 4 for the html changes.
"""

import pandas as pd
import os
import bs4
import changelog.py
import allEntries

__author__ = "Robbie Freeman"
__credits__ = ["Thomas Duffy"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

# Take in a new excel sheet. Read in the data using Pandas. Make it the new
# master sheet
if !os.path.isfile("static/downloads/newSheet.xlsx") :
    return False
newData = pd.read_excel("static/downloads/newSheet.xlsx", skip_blank_lines=True, skipinitialspace=True)
currentData = pd.read_csv("static/downloads/single-crystal_db.csv", header=4, skip_blank_lines=True, skipinitialspace=True)


# Check for validity. Return the error if invalid. TODO expand checks
assert(len(newData.columns) == len(currentData.columns))

# Compare the new data with the data already in the master sheet to determine
# the nature of the changes TODO implement
changes = []
if len(newData.index) == len(currentData.index):
    changes.append("Updated current minerals")
elif len(newData.index) > len(currentData.index):
    changes.append("Added minerals")
elif len(newData.index) < len(currentData.index):
    changes.append("Removed minerals")

# Delete the master and use the new sheet as the current master
os.remove("static/downloads/single-crystal_db.xlsx")
os.remove("static/downloads/single-crystal_db.csv")
os.rename("static/downloads/newSheet.xlsx", "static/downloads/single-crystal_db.xlsx")
newData.to_csv("static/downloads/single-crystal_db.csv")
os.remove("static/downloads/newSheet.xlsx")

# Log the changes
changelog(changes)

# Update the entries.html page (or at least the string that holds its data)
allEntries()



# return True, as changes were successfully made
return True
