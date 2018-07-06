import pandas as pd
import math

def main():
    # Read in the DB
    table = pd.read_csv("static/downloads/single-crystal_db.csv", usecols=[0, 1, 2], header=3, skip_blank_lines=True, skipinitialspace=True)

    # Get rid of all lines with NaN values
    for x in range(len(table.index)):
        if table.loc[x].isnull().values.any():
            table.drop(x, inplace=True)

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

    #editedTable = table.to_string(index=False)
    editedTable = editedTable[:-1]
    print(editedTable)
    return editedTable
