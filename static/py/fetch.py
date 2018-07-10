import pandas as pd
import math
import numpy

def isSelected(formData, str, catList) :
    if formData.get(str) != None:
        print (str + " is selected")
        catList.append(str)
        return (str, True)
    else:
        return (str, False)

# Take in a request.form (ImmutableMultiDict) that is from search.html
def main(formData) : # TODO: Generalize to work with all data in the spreadsheet
    # Save the strings of the chosen mineral classes and types in a list
    selectedClasses = []
    silicates = isSelected(formData, 'Silicates', selectedClasses)
    if not silicates:
        garnet = isSelected(formData, 'Garnet', selectedClasses)
        spinel = isSelected(formData, 'Spinel', selectedClasses)
        zeolite = isSelected(formData, 'Zeolite', selectedClasses)
        eulytine = isSelected(formData, 'Eulytine', selectedClasses)
    else:
        garnet = ('Garnet', True)
        spinel = ('Spinel', True)
        zeolite = ('Zeolite', True)
        eulytine = ('Eulytine', True)
    oxides = isSelected(formData, 'Oxides', selectedClasses)
    halides = isSelected(formData, 'Halides', selectedClasses)
    sulfides = isSelected(formData, 'Sulfides', selectedClasses)
    nitrates = isSelected(formData, 'Nitrates', selectedClasses)
    carbonAndCarbides = isSelected(formData, 'Carbon and Carbides', selectedClasses)
    nitrides = isSelected(formData, 'Nitrides', selectedClasses)
    phosphides = isSelected(formData, 'Phosphides', selectedClasses)

    # Save the strings of desired properties to be retrieved in a second list
    selectedProperties = []
    all = isSelected(formData, 'all_cats', selectedProperties)
    if not all:
        aem = isSelected(formData, 'aem', selectedProperties)
        am = isSelected(formData, 'am', selectedProperties)
        if not am:
            vrh = isSelected(formData, 'vrh', selectedProperties)
            vrb = isSelected(formData, 'vrb', selectedProperties)
            hsb = isSelected(formData, 'hsb', selectedProperties)
            ympr = isSelected(formData, 'ympr', selectedProperties)
        else:
            vrh = ("vrh", True)
            vrb = ("vrb", True)
            hsb = ("hsb", True)
            ympr = ("ympr", True)
        sv = isSelected(formData, 'sv', selectedProperties)
        svr = isSelected(formData, 'svr', selectedProperties)
        nm = isSelected(formData, 'nm', selectedProperties)
        af = isSelected(formData, 'af', selectedProperties)
        ec = isSelected(formData, 'ec', selectedProperties)
        pre = isSelected(formData, 'pre', selectedProperties)
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

    # Search the master sheet for any minerals that fit by class, then by type TODO: expand to general case
    table = pd.read_csv("static/downloads/single-crystal_db.csv", header=3, skip_blank_lines=True, skipinitialspace=True)

    # Get rid of all lines with all NaN values (not including class labels)
    table.dropna(inplace=True, how="all", axis=1) # columns
    table.dropna(inplace=True, how="all")         # rows

    # Select all rows for each mineral class, assuming they are accurately
    # grouped under their labels, and collect them in their respective
    # dataframes
    lastLabel = ''
    results = pd.DataFrame(columns=table.columns)
    classdf = pd.DataFrame(columns=table.columns)
    for index, row in table.iterrows(): # for each of the rows
        rowdf = row.to_frame()
        # if it's a row with a mineral class label
        if not (pd.isnull(row['Name'])) and pd.isnull(row['Composition']) and lastLabel != row['Name']:
            lastLabel = row['Name']
            if not classdf.equals(results):
                results = pd.concat([results, classdf], sort=False)
                classdf = pd.DataFrame(columns=table.columns)
        # if it's a row following a label but not a label itself
        elif lastLabel != '' and lastLabel in selectedClasses:
            classdf = pd.concat([rowdf.T, classdf]) # transpose of row because pandas stores it as a column
        # if it's a label but it's not being searched for
        elif lastLabel not in selectedClasses:
            lastLabel = ''
        # if it's a case that's unaccounted for
        else:
            print(":( something went wrong or was unexpected at line " + str(index))
    results = pd.concat([results, classdf], sort=False) # for the final category

    print(results)

    # Read the selected properties of the matching minerals into a Pandas
    # DataFrame
    # Assumes all values are selected initially and removes the appropriate
    # column(s) if a category isn't
    if all[0] not in selectedProperties:
        if aem[0] not in selectedProperties:
            results.drop('11', axis=1)
            results.drop('44', axis=1)
            results.drop('12', axis=1)
        if am[0] not in selectedProperties:
            if vrh[0] not in selectedProperties:
                results.drop('K', axis=1)
                results.drop('G', axis=1)
                results.drop('K/G', axis=1) # TODO Should more be here?
            if vrb[0] not in selectedProperties:
                results.drop('GR', axis=1)
                results.drop('GV', axis=1)
            if hsb[0] not in selectedProperties:
                results.drop('GHS1', axis=1)
                results.drop('GHS2', axis=1)
                results.drop('GHSA', axis=1)
            if ympr[0] not in selectedProperties:
                results.drop('nVRH', axis=1) # TODO Should these be here?
                results.drop('EVRH', axis=1)
        if sv[0] not in selectedProperties:
            results.drop('VP', axis=1)
            results.drop('VB', axis=1)
            results.drop('VS', axis=1)
        if svr[0] not in selectedProperties:
            results.drop('VP/VS', axis=1) # TODO add in VB/VS AND K/G
        if nm[0] not in selectedProperties:
            results.drop('C12/C11', axis=1)
            results.drop('C44/C11', axis=1)
        if af[0] not in selectedProperties:
            results.drop('AZ', axis=1)
            results.drop('AU', axis=1)
            results.drop('AL', axis=1)
            results.drop('AG', axis=1)
        if ec[0] not in selectedProperties:
            results.drop('S11', axis=1)
            results.drop('S12', axis=1)
            results.drop('S44', axis=1)
        if pre[0] not in selectedProperties:
            results.drop('n_110', axis=1)
            results.drop('n_001', axis=1)
    else:
        print("all properties included")

    # Format the DataFrame to be read into the js file

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
