"""Script that checks for changes uploaded to the database by Tom through
FileZilla and updates the master sheet to be the new sheet. Then, it alters the
changelog.html file to reflect the changes. Uses pandas for the table changes
and Beautiful Soup 4 for the html changes.
"""

import pandas as pd
import os
import bs4
import sys

import tableManager

__author__ = "Robbie Freeman"
__credits__ = ["Thomas Duffy"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

def main():

    # Take in a new excel sheet. Read in the data using Pandas. Make it the new
    # master sheet
    """if not os.path.isfile("static/downloads/newSheet.xlsx") :
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
        changes.append("Removed minerals")"""

    tables = tableManager.getInitialTables()
    table =  pd.read_excel("static/downloads/single-crystal_db_complete.xlsx", sheetname="Cubic", header=4, skip_blank_lines=True, skipinitialspace=True)

    # Create the CSV file from the original, master excel sheet
    if os.path.isfile('static/downloads/single-crystal_db_complete.csv') :
        os.remove("static/downloads/single-crystal_db_complete.csv")
    table.to_csv('static/downloads/single-crystal_db_complete.csv', index=False)

    # Find the mineral group and structure categories and log them in mineralCats.txt
    # for generating search.html
    # Scan through each row looking for unique mineral classes and unique structures
    # within each
    lastLabel = ''
    categories = [] # list of tuples of the form (class, structure)
    classdf = pd.DataFrame(columns=table.columns)
    for index, row in table.iterrows(): # for each of the rows
        rowdf = row.to_frame() # Dataframe of row, which is normally a Series
        lastLabel = lastLabel.replace(" ","&#160;") # account for spaces in classes (NOT structures)
        if isinstance(row['Structure/SG'], str):
            structure = row['Structure/SG'].split(',')[0]
        # if it's a row with a mineral class label
        if not (pd.isnull(row['Name'])) and pd.isnull(row['Composition']) and lastLabel != row['Name']:
            lastLabel = row['Name']
        # if it's a row following a label but not a label itself
        elif lastLabel != '' and (lastLabel, structure) not in categories:
            categories.append((lastLabel, structure))
    print(categories)
    if os.path.isfile("static/text/categories.txt") :
        os.remove("static/text/categories.txt")
    orig_stdout = sys.stdout
    file = open('static/text/categories.txt', 'w')
    sys.stdout = file
    print(categories, end='')
    sys.stdout = orig_stdout
    file.close()

    """# Delete the master and use the new sheet as the current master
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
    return True"""
