import pandas as pd
import math

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
        else:
            vrh = ("vrh", True)
            vrb = ("vrb", True)
            hsb = ("hsb", True)
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
        sv = ("sv", True)
        svr = ("svr", True)
        nm = ("nm", True)
        af = ("af", True)
        ec = ("ec", True)
        pre = ("pre", True)

    # Search the master sheet for any minerals that fit by class, then by type TODO: expand to general case
    table = pd.read_csv("static/downloads/single-crystal_db.csv", header=3, skip_blank_lines=True, skipinitialspace=True)

    # Get rid of all lines with NaN values
    table = table.drop('Unnamed: 30', axis=1)   # columns
    table = table.drop('Unnamed: 33', axis=1)
    for x in range(len(table.index)):           # rows
        if table.loc[x].isnull().values.any():
            table.drop(x, inplace=True)

    results = pd.DataFrame(columns=table.columns)
    print(results)
    if silicates[1] == True:
        results = pd.concat([results, table[table['Group'].str.contains(silicates[0][:-1]) == True]])
        numResults = len(results)
    if oxides[1] == True:
        results = pd.concat([results, table[table['Group'].str.contains(oxides[0][:-1]) == True]])
        numResults = len(results)
    if halides[1] == True:
        results = pd.concat([results, table[table['Group'].str.contains(halides[0][:-1]) == True]])
        numResults = len(results)
    if sulfides[1] == True:
        results = pd.concat([results, table[table['Group'].str.contains(sulfides[0][:-1]) == True]])
        numResults = len(results)
    if nitrates[1] == True:
        results = pd.concat([results, table[table['Group'].str.contains(nitrates[0][:-1]) == True]])
        numResults = len(results)
    if carbonAndCarbides[1] == True:
        results = pd.concat([results, table[table['Group'].str.contains(carbonAndCarbides[0][:-1]) == True]])
        numResults = len(results)
    if nitrides[1] == True:
        results = pd.concat([results, table[table['Group'].str.contains(nitrides[0][:-1]) == True]])
        numResults = len(results)
    if phosphides[1] == True:
        results = pd.concat([results, table[table['Group'].str.contains(phosphides[0][:-1]) == True]])
        numResults = len(results)

    # Read the selected properties of the matching minerals into a Pandas DataFrame
    #if aem[1] == true:
        #table

    # Format the DataFrame to be read into the js file

    resultString = results.to_string()
    if resultString == "":
        resultString = 'No results found'
    else:
        resultString = ""
        results.insert(len(results.columns), "\\\\\\", "\\\\\\")
        for x in range(len(results.index)):
            print("y-coord: " + str(x))
            for y in range(len(results.columns)):
                cell = results.iloc[x, y]
                if type(cell) != str:
                    cell = str(cell)
                if y != len(results.columns) - 1:
                    resultString += cell + "~*"
                else:
                    resultString += cell
        resultString = resultString[:-1]
    # Return the DataFrame
    return resultString
