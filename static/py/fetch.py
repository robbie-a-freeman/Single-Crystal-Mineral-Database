"""Performs the searching accessible in search.html and the fetching for individual
minerals when called. search() is specifically for data coming from search.html, while
getMineral() is specifically for individual mineral results. All the other functions
are basically helper functions. Uses pandas and a bit of numpy for table manipulation.
"""

import pandas as pd
import math
import numpy
import xlrd
import re
from flask import jsonify

import tableManager

__author__ = "Robbie Freeman"
__credits__ = ["Thomas Duffy"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

results = None

# Return the results table. Shouldn't be called before search()
def getResultsTable() :
    return results

# Return the selected properties list. Shouldn't be called before search()
def getSelectedProperties() :
    return selectedProperties

# Return the column name list. Shouldn't be called before search()
def getColumnNames() :
    return columnLabels

# Check if the exact string is selected. Return a boolean
def isSelected(formData, query) :
    if formData.get(query) != None or formData.get('\'all-minerals\'') != None:
        return True
    else:
        return False

# Check if the given element or any subelement is selected. Return a boolean
def isPresent(formData, query) :
    fullQuery = '\'' + query
    stringifiedData = str(formData)
    if stringifiedData.find(fullQuery) != -1 or formData.get('\'all-minerals\'') != None:
        return True
    else:
        return False

# Determine if str has a checkbox in formData that is selected. If so, add to
# the given lists and return a tuple with True. Otherwise, return a tuple with
# False. For properties
def isSelectedProperties(formData, str, catList) :
    if formData.get(str) != None:
        catList.append(str)
        return (str, True)
    else:
        return (str, False)

# Checks if the name of a specific "category", "group", or "structure" (the possible values
# of the string type) are contained in the 3 lists given, assuming the same format
# of lists as "all-minerals_CATEGORY_GROUP_STRUCTURE". Returns boolean

# TODO cleanup, kind of cumbersome
def containsElement(type, name, categories, groups, structures):
    regexPattern = re.compile(name)
    if type is "category":
        if name in categories:
            return True
        elif filter(regexPattern.match, groups) != None:
            return True
        elif filter(regexPattern.match, structures) != None:
            return True
        else:
            return False
    elif type is "group":
        if name in groups:
            return True
        elif filter(regexPattern.match, structures) != None:
            return True
        else:
            return False
    elif type is "structure":
        if name in structures:
            return True
        else:
            return False
    else:
        raise NameError('Invalid type name in containsElement()')

# Take in a request.form (ImmutableMultiDict) that is from search.html
def search(formData) :
    # Save the strings of the chosen mineral classes and types in a list
    print("formData")
    print(formData)

    # ex. CS1[('G1', 'S1'), ('G2', 'S2')]CS2[('G1', 'S3'), ('G3', 'S4')]
    # ->  (CS1,'G1','S1'),(CS1,'G2','S2'),(CS2,'G1','S3'),(CS2,'G3','S4')
    # dupes and whitespace should be removed
    file = open('static/text/categories.txt', 'r')
    allCategories = file.read()
    allCategories = allCategories.replace("&#160;", " ")
    print("allCategories")
    print(allCategories)

    # Check which class/structures are desired against the ones that exist.
    # Creates the fetchedCategories, fetchedGroups, and fetchedStructures lists,
    # which store the search criteria for later. Also logs which sheets to open,
    # which saves time in retrieval
    # Reminder: Categories > Groups > Structures
    sheetsToCheck = []
    fetchedCategories = []
    fetchedGroups = []
    fetchedStructures = []
    numberOfCategories = len(allCategories.split('[')) - 1
    assert(numberOfCategories > 0)
    for i in range(numberOfCategories):
        if i < 1:
            currentCategory = "all-minerals_" + allCategories.split('[')[i].lower()
        else:
            currentCategory = "all-minerals_" + allCategories.split(']')[i].split('[')[0].lower()
        if isPresent(formData, currentCategory): # if some subset of the category is selected
            assert(currentCategory not in fetchedCategories)
            sheetsToCheck.append(currentCategory.split('_')[1].capitalize())
            if isSelected(formData, currentCategory): # if the category box is selected, and thus all its children
                fetchedCategories.append(currentCategory)
            else: # if category box isn't selected, but some of its children are
                currentCategoryContent = allCategories.split('[')[i+1].split(']')[0]
                numberOfGroups = len(currentCategoryContent.split('\',')) - 1
                assert(numberOfGroups > 0)
                for j in range(numberOfGroups):
                    currentGroup = currentCategoryContent.split('(\'')[j+1].split('\',')[0].lower()
                    fullCurrentGroup = currentCategory + '_' + currentGroup
                    if isPresent(formData, fullCurrentGroup) and fullCurrentGroup not in fetchedGroups: # no duplicate groups
                        if isSelected(formData, fullCurrentGroup):
                            fetchedGroups.append(fullCurrentGroup)
                        else:
                            # number of nonunique groups is = to number of structures
                            # one structure per group
                            currentStructure = currentCategoryContent.split(', \'')[j+1].split('\')')[0].lower()
                            fullCurrentStructure = fullCurrentGroup + '_' + currentStructure
                            assert(fullCurrentStructure not in fetchedStructures)
                            fetchedStructures.append(fullCurrentStructure)

    print(fetchedCategories)
    print(fetchedGroups)
    print(fetchedStructures)
    print(sheetsToCheck)

    # Grab the initial tables from the spreadsheet
    tables = tableManager.getInitialTables(asOne=False)
    tableNames = tableManager.getTableNames(filterRefs=True)
    #table =  pd.read_excel("static/downloads/single-crystal_db_complete.xlsx", sheet_name="Cubic", header=4, skip_blank_lines=True, skipinitialspace=True)
    #table.dropna(inplace=True, how="all", axis=1) # columns
    #table.dropna(inplace=True, how="all", axis=0) # rows

    # Select all rows for each mineral class, assuming they are accurately
    # grouped under their labels, and collect them in their respective
    # dataframes. Also account for structure filters
    # TODO adjust based on selected tables
    lastMineralCat = ""
    lastMineralGroup = ""
    resultTables = []
    structure = ""
    for tn in range(len(sheetsToCheck)):
        results = pd.DataFrame(columns=tables[tn].columns)
        classdf = pd.DataFrame(columns=tables[tn].columns)
        lastMineralCat = sheetsToCheck[tn]
        print(tableNames)
        print(len(tables))
        table = tables[tableNames.index(lastMineralCat)] # retrieve table by index
        for index, row in table.iterrows(): # for each of the rows in selected table
            rowdf = row.to_frame() # turns a row (Series) into DataFrame
            if isinstance(row['Structure/SG'], str):
                structure = "all-minerals_" + lastMineralCat.lower() + '_' + lastMineralGroup.lower() + '_' + row['Structure/SG'].split(',')[0].lower()
                #print(structure)
            # if mineral category is requested at all
            if isPresent(formData, "all-minerals_" + lastMineralCat.lower()) :
                # if it's a row with a mineral group label we are looking for
                if not (pd.isnull(row['Name'])) and pd.isnull(row['Composition']) and lastMineralGroup != row['Name']:
                    lastMineralGroup = row['Name']
                    if not classdf.equals(results):
                        results = pd.concat([classdf, results], sort=False)
                        classdf = pd.DataFrame(columns=table.columns)
                # if it's a row with an element we are looking for
                elif lastMineralGroup != '' and (isPresent(formData, "all-minerals_" + lastMineralCat.lower() + lastMineralGroup.lower()) or isPresent(formData, structure)):
                    classdf = pd.concat([classdf, rowdf.T]) # transpose of row because pandas stores it as a column
                # if it's a case that's unaccounted for
                else:
                    #print(structure.split('_')[1])
                    print("Hopefully not something we care about at line " + structure)
        results = pd.concat([results, classdf], sort=False) # for the final category
        resultTables.append(results)

    # Save the strings of desired properties to be retrieved in a second list
    # selectedProperties list defined above
    global selectedProperties
    selectedProperties = []
    allCats = isSelectedProperties(formData, 'all_cats', selectedProperties)
    if not allCats[1]:
        aem = isSelectedProperties(formData, 'aem', selectedProperties)
        am = isSelectedProperties(formData, 'am', selectedProperties)
        if not am[1]:
            vrh = isSelectedProperties(formData, 'vrh', selectedProperties)
            vrb = isSelectedProperties(formData, 'vrb', selectedProperties)
            hsb = isSelectedProperties(formData, 'hsb', selectedProperties)
            ympr = isSelectedProperties(formData, 'ympr', selectedProperties)
        else:
            vrh = ("vrh", True)
            vrb = ("vrb", True)
            hsb = ("hsb", True)
            ympr = ("ympr", True)
        sv = isSelectedProperties(formData, 'sv', selectedProperties)
        svr = isSelectedProperties(formData, 'svr', selectedProperties)
        nm = isSelectedProperties(formData, 'nm', selectedProperties)
        af = isSelectedProperties(formData, 'af', selectedProperties)
        ec = isSelectedProperties(formData, 'ec', selectedProperties)
        pre = isSelectedProperties(formData, 'pre', selectedProperties)
    else:
        aem = ("aem", True)
        am = ("am", True)
        vrh = ("vrh", True)
        vrb = ("vrb", True)
        hsb = ("hsb", True)
        ympr = ("ympr", True)
        sv = ("sv", True)
        svr = ("svr", True)
        nm = ("nm", True)
        af = ("af", True)
        ec = ("ec", True)
        pre = ("pre", True)

    # Read the selected properties of the matching minerals into a Pandas DataFrame
    # Assumes all values are selected initially and removes the appropriate
    # column(s) if a category isn't
    for t in resultTables:
        if not t.empty:
            if allCats[0] not in selectedProperties:
                # print(list(t))
                if aem[0] not in selectedProperties:
                    t = t.drop(11, axis=1)
                    t = t.drop(44, axis=1)
                    t = t.drop(12, axis=1)
                if am[0] not in selectedProperties:
                    if vrh[0] not in selectedProperties:
                        t = t.drop('K', axis=1)
                        t = t.drop('G', axis=1)
                        t = t.drop('K/G', axis=1)
                    if vrb[0] not in selectedProperties:
                        t = t.drop('GR', axis=1)
                        t = t.drop('GV', axis=1)
                    if hsb[0] not in selectedProperties:
                        t = t.drop('GHS1', axis=1)
                        t = t.drop('GHS2', axis=1)
                        t = t.drop('GHSA', axis=1)
                    if ympr[0] not in selectedProperties:
                        t = t.drop('nVRH', axis=1)
                        t = t.drop('EVRH', axis=1)
                if sv[0] not in selectedProperties:
                    t = t.drop('VP', axis=1)
                    t = t.drop('VB', axis=1)
                    t = t.drop('VS', axis=1)
                if svr[0] not in selectedProperties:
                    t = t.drop('VP/VS', axis=1)
                if nm[0] not in selectedProperties:
                    t = t.drop('C12/C11', axis=1)
                    t = t.drop('C44/C11', axis=1)
                if af[0] not in selectedProperties:
                    t = t.drop('AZ', axis=1)
                    t = t.drop('AU', axis=1)
                    t = t.drop('AL', axis=1)
                    t = t.drop('AG', axis=1)
                if ec[0] not in selectedProperties:
                    t = t.drop('S11', axis=1)
                    t = t.drop('S44', axis=1)
                    t = t.drop('S12', axis=1)
                if pre[0] not in selectedProperties:
                    t = t.drop('n_110', axis=1)
                    t = t.drop('n_001', axis=1)
            else:
                print("all properties included")

        # Get rid of label rows
        t.dropna(inplace=True, thresh=15, axis=0)
    setGlobalColumns(resultTables[0]) # TODO fix
    setGlobalResultTable(resultTables)
    for t in resultTables:
        t = t.to_json()
    return resultTables # formatString(results)

# sets the properties for the given table for the global variable selectedProperties
def setGlobalResultTable(resultTables):
    global results
    results = resultTables

# sets the column labels for the given table for the global variable columnLabels
def setGlobalColumns(table):
    global columnLabels
    columnLabels = list(table);

# sets the properties for the given table for the global variable selectedProperties
def setGlobalProperties(properties):
    global selectedProperties
    selectedProperties = properties;

# Drops the column with the name given from the given pandas table
def drop(name, table):
    if table[[name]] != None:
        table = results.drop(name, axis=1)

# takes in the row num of the mineral and returns the name of the sheet of origin
def getSheetNameOfMineral(rowNum):
    # Store the number of elements in each sheet of the spreadsheet, i.e. how many
    # minerals of one type are there, in a list of all the first indices and a
    # parallel list of names of each type (for example: "cubic" or "hexagonal").
    # This will be sent to the client along with the other data in the string form
    sheetIndices = tableManager.getTableIntervals()
    sheetNames = tableManager.getTableNames()
    for i in range(len(sheetIndices)):
        if rowNum <= sheetIndices[i]:
            return sheetNames[i]
    return "ROW NUM NOT FOUND IN A SHEET"


# Format the results dataframe that is passed in to fit with the JS file that
# will receive and parse it.
def formatString(results):
    # Format the DataFrame to be read into the js file
    print(results)
    resultString = results.to_string()
    if resultString == "":
        resultString = "No results found"
    else:
        resultString = ""
        results.insert(len(results.columns), "\\\\\\", "\\\\\\")
        for x in range(len(results.index)):
            # insert the sheetname of origin
            #resultString += getSheetNameOfMineral(x) + "~*"
            #print("FINISHED GETTING SHEETNAMES")
            # insert each cell y in a given row x
            for y in range(len(results.columns)):
                cell = results.iloc[x, y]
                if type(cell) != str:
                    # truncate all floats at 4 places except densities
                    if type(cell) == float:
                        cell = round(cell, 4)
                    cell = str(cell)
                if y != len(results.columns) - 1:
                    resultString += cell + "~*" # this is the arbitrarily set
                else:                           # cell separator expected by the
                    resultString += cell        # js file
        resultString = resultString[:-1]
    # Return the DataFrame
    return resultString

# Quickly locate and grab a specific mineral and all of its information
def getMineral(num):
    # Find if a mineral matches the given composition. If it does, return the
    # row. If not, return null.
    num = int(num)
    tables = tableManager.getInitialTables(asOne=False)
    print("START OF TABLES")
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(tables)
    tableLengths = []
    for t in range(len(tables)):
        tables[t] = tables[t].drop([0]) # drop the Silicates (or equivalent) line specifically, since it has
                                # units in it and does not fit the same criteria as
                                # other rows being dropped.
        tables[t].dropna(inplace=True, how="any", axis=0, thresh=5) # drop other label rows
        tableLengths.append(len(tables[t].index))
    for t in range(len(tables)):
        if num - tableLengths[t] < 0:
            result = tables[t].iloc[[num]]
            return formatString(result)
        else:
            num = num - tableLengths[t]
    return "Error: no result found with input number"
'''
    table = pd.read_excel("static/downloads/single-crystal_db_complete.xlsx", sheet_name="Cubic", header=4, skip_blank_lines=True, skipinitialspace=True)

    # Format the row as a String and return it. Also update columns and properties

    table = table.drop([0]) # drop the Silicates line specifically, since it has
                            # units in it and does not fit the same criteria as
                            # other rows being dropped.
    table.dropna(inplace=True, how="any", axis=0, thresh=5) # drop other label rows
    print(table)
    result = table.iloc[[rowNum]]

    setGlobalProperties(['all_cats'])
    setGlobalColumns(result.columns)
    setGlobalResultTable(result)
    return formatString(result)
    '''
