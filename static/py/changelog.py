"""Script that  alters the changelog.html file to reflect changes originally
logged by changeHandler.py. Uses pandas for the table changes and Beautiful Soup
4 for the html changes.
"""

import pandas as pd
import os.path
import bs4
import sys
import xlrd

__author__ = "Robbie Freeman"
__credits__ = ["Thomas Duffy"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

# Update changelog.html to reflect the changes using Beautiful Soup. Put the
# changes at the top of the page #TODO test rigorously

#print(sys.argv[1])
#print(sys.argv[2])

with open("changelog.html") as inf:
    txt = inf.read()
    soup = bs4.BeautifulSoup(txt)
change = soup.new_tag("p")
ptag.insert(0, NavigableString("test change"))
soup.body.append(change) #TODO update position, it's not within proper containers
with open("changelog.html", "w") as outf:
    outf.write(str(soup))
