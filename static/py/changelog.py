"""Script that checks for changes uploaded to the database by Tom through
FileZilla and updates the master sheet with the changes. Then, it alters the
changelog.html file to reflect the changes. Uses pandas for the table changes 
and Beautiful Soup 4 for the html changes.
"""

import pandas as pd
import os.path
import bs4

__author__ = "Robbie Freeman"
__credits__ = ["Thomas Duffy"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

# Take in a new excel sheet. Read in the data using Pandas. TODO update with master
if !os.path.isfile("static/downloads/newSheet.xlsv") :
    return False
newData = pd.read_excel("static/downloads/newSheet.xlsv", skip_blank_lines=True, skipinitialspace=True)
currentData = pd.read_csv("static/downloads/single-crystal_db.csv", header=4, skip_blank_lines=True, skipinitialspace=True)

# Check for validity. Return the error if invalid. TODO expand checks
assert(len(newData.columns) == len(currentData.columns))
# Compare the new data with the data already in the master sheet TODO implement

# Add in the new data to the current dataset. Save new sheet
currentData = currentData.append(newData)

# Update changelog.html to reflect the changes using Beautiful Soup. Put the
# changes at the top of the page #TODO test rigorously
with open("changelog.html") as inf:
    txt = inf.read()
    soup = bs4.BeautifulSoup(txt)
change = soup.new_tag("p")
ptag.insert(0, NavigableString("test change"))
soup.body.append(change) #TODO update position, it's not within proper containers
with open("changelog.html", "w") as outf:
    outf.write(str(soup))

# return True, as changes were successfully made
return True
