"""Performs the searching accessible in search.html and the fetching for individual
minerals when called. search() is specifically for data coming from search.html, while
getMineral() is specifically for individual mineral results. All the other functions
are basically helper functions. Uses pandas and a bit of numpy for table manipulation.
"""

import pandas as pd
import math
import numpy

import tableManager

__author__ = "Robbie Freeman"
__credits__ = ["Thomas Duffy"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

selectedProperties = []
columnLabels = []
results = None

# Return the selected properties list. Shouldn't be called before search()
def getSelectedProperties() :
    return selectedProperties

# Return the column name list. Shouldn't be called before search()
def getColumnNames() :
    return columnLabels

# Return the results table. Shouldn't be called before search()
def getResultsTable() :
    return results

# Determine if str has a checkbox in formData that is selected. If so, add to
# the given lists and return a tuple with True. Otherwise, return a tuple with
# False. For categories
def isSelected(formData, str, classList, structList) :
    if formData.get(str) != None or formData.get('all_minerals') != None:
        print (str + " is selected")
        if str.split('_')[0] not in classList:
            classList.append(str.split('_')[0])
        structList.append(str)
        return (str, True)
    else:
        return (str, False)

# Determine if str has a checkbox in formData that is selected. If so, add to
# the given lists and return a tuple with True. Otherwise, return a tuple with
# False. For properties
def isSelectedProperties(formData, str, catList) :
    if formData.get(str) != None:
        print (str + " is selected")
        catList.append(str)
        return (str, True)
    else:
        return (str, False)

# Take in a request.form (ImmutableMultiDict) that is from search.html
def search(formData) : # TODO: Generalize to work with all data in the spreadsheet
    # Save the strings of the chosen mineral classes and types in a list
    # TODO: utilize the select all checkbox for minerals

    print(formData)

    selectedClasses = []
    selectedStructures = []

    silicates = isSelected(formData, 'Silicates_all', selectedClasses, selectedStructures)
    if not silicates[1]:
        garnet = isSelected(formData, 'Silicates_Garnet', selectedClasses, selectedStructures)
        spinel = isSelected(formData, 'Silicates_Spinel', selectedClasses, selectedStructures)
        zeolite = isSelected(formData, 'Silicates_Zeolite', selectedClasses, selectedStructures)
        eulytine = isSelected(formData, 'Silicates_Eulytine', selectedClasses, selectedStructures)
    else:
        garnet = (silicates[0] + 'Silicates_Garnet', True)
        spinel = (silicates[0] + 'Silicates_Spinel', True)
        zeolite = (silicates[0] + 'Silicates_Zeolite', True)
        eulytine = (silicates[0] + 'Silicates_Eulytine', True)
    oxides = isSelected(formData, 'Oxides_all', selectedClasses, selectedStructures)
    halides = isSelected(formData, 'Halides_all', selectedClasses, selectedStructures)
    sulfides = isSelected(formData, 'Sulfides_all', selectedClasses, selectedStructures)
    nitrates = isSelected(formData, 'Nitrates_all', selectedClasses, selectedStructures)
    carbonAndCarbides = isSelected(formData, 'Carbon and Carbides_all', selectedClasses, selectedStructures)
    nitrides = isSelected(formData, 'Nitrides_all', selectedClasses, selectedStructures)
    phosphides = isSelected(formData, 'Phosphides_all', selectedClasses, selectedStructures)

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

    table = tableManager.getInitialTable()

    # Select all rows for each mineral class, assuming they are accurately
    # grouped under their labels, and collect them in their respective
    # dataframes. Also account for structure filters
    lastLabel = ''
    results = pd.DataFrame(columns=table.columns)
    classdf = pd.DataFrame(columns=table.columns)
    for index, row in table.iterrows(): # for each of the rows
        rowdf = row.to_frame() # Dataframe of row, which is normally a Series
        if isinstance(row['Structure/SG'], str):
            structure = lastLabel + '_' + row['Structure/SG'].split(',')[0]
        # if it's a row with a mineral class label
        if not (pd.isnull(row['Name'])) and pd.isnull(row['Composition']) and lastLabel != row['Name']:
            lastLabel = row['Name']
            if not classdf.equals(results):
                results = pd.concat([results, classdf], sort=False)
                classdf = pd.DataFrame(columns=table.columns)
        # if it's a row following a label but not a label itself
        elif lastLabel != '' and lastLabel in selectedClasses and (structure in selectedStructures or lastLabel + '_all' in selectedStructures):
            classdf = pd.concat([rowdf.T, classdf]) # transpose of row because pandas stores it as a column
        # if it's a label but it's not being searched for
        elif lastLabel not in selectedClasses:
            lastLabel = ''
        # if it's a case that's unaccounted for
        else:
            print(structure.split('_')[1])
            print(":( something went wrong or was unexpected at line " + str(index))
    results = pd.concat([results, classdf], sort=False) # for the final category

    # Read the selected properties of the matching minerals into a Pandas
    # DataFrame
    # Assumes all values are selected initially and removes the appropriate
    # column(s) if a category isn't
    if allCats[0] not in selectedProperties:
        if aem[0] not in selectedProperties:
            results.drop('11', axis=1)
            results.drop('44', axis=1)
            results.drop('12', axis=1)
        if am[0] not in selectedProperties:
            if vrh[0] not in selectedProperties:
                results = results.drop('K', axis=1)
                results = results.drop('G', axis=1)
                results = results.drop('K/G', axis=1)
            if vrb[0] not in selectedProperties:
                results = results.drop('GR', axis=1)
                results = results.drop('GV', axis=1)
            if hsb[0] not in selectedProperties:
                results = results.drop('GHS1', axis=1)
                results = results.drop('GHS2', axis=1)
                results = results.drop('GHSA', axis=1)
            if ympr[0] not in selectedProperties:
                results = results.drop('nVRH', axis=1)
                results = results.drop('EVRH', axis=1)
        if sv[0] not in selectedProperties:
            results = results.drop('VP', axis=1)
            results = results.drop('VB', axis=1)
            results = results.drop('VS', axis=1)
        if svr[0] not in selectedProperties:
            results = results.drop('VP/VS', axis=1)
        if nm[0] not in selectedProperties:
            results = results.drop('C12/C11', axis=1)
            results = results.drop('C44/C11', axis=1)
        if af[0] not in selectedProperties:
            results = results.drop('AZ', axis=1)
            results = results.drop('AU', axis=1)
            results = results.drop('AL', axis=1)
            results = results.drop('AG', axis=1)
        if ec[0] not in selectedProperties:
            results = results.drop('S11', axis=1)
            results = results.drop('S44', axis=1)
            results = results.drop('S12', axis=1)
        if pre[0] not in selectedProperties:
            results = results.drop('n_110', axis=1)
            results = results.drop('n_001', axis=1)
    else:
        print("all properties included")

    # Get rid of label rows
    results.dropna(inplace=True, how="any", axis=0)

    print(len(results))
    setGlobalColumns(results)
    setGlobalResultTable(results)
    return formatString(results);

# sets the column labels for the given table for the global variable columnLabels
def setGlobalColumns(table):
    global columnLabels
    columnLabels = list(table);

# sets the properties for the given table for the global variable selectedProperties
def setGlobalProperties(properties):
    global selectedProperties
    selectedProperties = properties;

# sets the properties for the given table for the global variable selectedProperties
def setGlobalResultTable(resultTable):
    global results
    results = resultTable;

# Format the results dataframe that is passed in to fit with the JS file that
# will receive and parse it.
def formatString(results):
    # Format the DataFrame to be read into the js file
    print(results)
    resultString = results.to_string()
    if resultString == "":
        resultString = 'No results found'
    else:
        resultString = ""
        results.insert(len(results.columns), "\\\\\\", "\\\\\\")
        for x in range(len(results.index)):
            for y in range(len(results.columns)):
                cell = results.iloc[x, y]
                if type(cell) != str:
                    cell = str(cell)
                if y != len(results.columns) - 1:
                    resultString += cell + "~*" # this is the arbitrarily set
                else:                           # cell separator expected by the
                    resultString += cell        # js file
        resultString = resultString[:-1]
    # Return the DataFrame
    return resultString

# Quickly locate and grab a specific mineral and all of its information
def getMineral(rowNum):
    # Find if a mineral matches the given composition. If it does, return the
    # row. If not, return null.
    table = tableManager.getInitialTable()

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
