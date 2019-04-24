"""Contains helper functions for loading the database.
"""

import pandas as pd
import os
import string
import xlrd

#import changelog
#import allEntries

__author__ = "Robbie Freeman"
__credits__ = ["Thomas Duffy"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

# Grab the excel file in the database, skip the the header line assuming it's still
# the fourth line in the sheet. Loads all sheets with data without the references
def getInitialTables(spreadsheet = "static/downloads/single-crystal_db_complete.xlsx", asOne = True):
    # load the file with the restrictions on columns to display publicly
    loadingRules = open('static/text/sheetLoadingControls.txt', 'r').read()
    loadingRules = loadingRules.replace(string.whitespace, '')
    loadingRules = loadingRules.replace('\n', '')
    rules = loadingRules.split(']')[:-1]
    sheets = [] # a list of the rule labels, which is each of the rules without
                # beginning asterisks. It's basically sheet names, global, and/or
                # noncubic
    columns = [] # a list of the lists of rules. Each index correlates to a the
                 # index in the list sheets.
    isNonCubicIncluded = True # default is true, but verifies below
    for r in rules:
        rule = r.split('[')
        columnNames = rule[1].split(',')
        if rule[0] == 'noncubic' and '*' in columnNames:
            isNonCubicIncluded = False
        if '*' in columnNames:
            continue
        if not isNonCubicIncluded:
            if rule[0] != 'Cubic':
                continue
        columnNames = filter(lambda name: name != '', columnNames)
        columns.append(columnNames)
        sheets.append(rule[0])

    assert(len(sheets) == len(columns))
    # iterate through the sheets, apply the column dropping rules, and return
    # the results
    tables = [] # array of tables from sheets
    xl = pd.ExcelFile(spreadsheet)
    isGlobalIncluded = 'global' in sheets
    for x in xl.sheet_names:
        if not "Refs" in x and not "Key" in x and x in sheets and isGlobalIncluded:
            # Cubic is the only sheet that has a messed up header by default
            if x == 'Cubic':
                table = xl.parse(sheet_name=x, header=4, skip_blank_lines=True, skipinitialspace=True)
            else:
                # TODO update header number for each of the possible sheets
                table = xl.parse(sheet_name=x, skip_blank_lines=True, skipinitialspace=True)
            # Get rid of all lines with all NaN values (not including class labels)
            table.dropna(inplace=True, how="all", axis=1) # columns
            table.dropna(inplace=True, how="all", axis=0) # rows
            # Get rid of specific columns that are not supposed to be publicly visible
            columnsToDrop = []
            if isGlobalIncluded:
                columnsToDrop.append(columns[0])
            if '*' in columns[sheets.index(x)]:
                break
            if x in sheets:
                columnsToDrop.append(columns[sheets.index(x)])
                for col in columnsToDrop:
                    table.drop(col, inplace=True, axis=1)
            tables.append(table)
    bigTable = pd.DataFrame(columns=tables[0].columns)
    # Problematic. TODO Need to fix to account for different sheet formats
    # Can a dataframe have multiple sheets in it?
    if asOne == True:
        bigTable = pd.concat(tables, sort=False) # not entirely sure what sort does
        return bigTable
    else:
        return tables

# Grab the excel file in the database. Loads all reference sheets and non-table
# pages. TODO filter with * in loadingRules.txt
def getReferences():
    tables = [] # array of tables from sheets
    xl = pd.ExcelFile("static/downloads/single-crystal_db_complete.xlsx")
    for x in xl.sheet_names:
        if x.contains("Refs") or x.contains("Key"):
            table = xl.parse(sheet_name=x, index=False, header=False)
            print(table)
            tables.append(table)
    return tables

# Get just the first three columns (Name, Comp, Group), of each sheet and return
# it as one. Doe not check for hidden information, as this information is kind
# of critical for each mineral
def getInitialTableQuick():
    # load the file with the restrictions on columns to display publicly
    loadingRules = open('static/text/sheetLoadingControls.txt', 'r').read()
    loadingRules = loadingRules.replace(string.whitespace, '')
    loadingRules = loadingRules.replace('\n', '') # not deleted with above line for some reason
    rules = loadingRules.split(']')[:-1]
    sheets = []
    columns = []
    for r in rules:
        rule = r.split('[')
        columnNames = rule[1].split(',')
        if '*' in columnNames:
            continue
        else:
            print(r)
            columns.append(columnNames)
            sheets.append(rule[0])
    assert(len(sheets) == len(columns))
    print(sheets)
    print(columns)

    # iterate through the sheets, apply the column dropping rules, and return
    # the results
    xl = pd.ExcelFile("static/downloads/single-crystal_db_complete.xlsx")
    tables = []
    isGlobalIncluded = 'global' in sheets
    isNonCubicIncluded = 'noncubic' in sheets
    if not isNonCubicIncluded:
        sheets = ['Cubic']
    if isGlobalIncluded:
        for x in xl.sheet_names:
            if not "Refs" in x and not "Key" in x and x in sheets:
                # Cubic is the only sheet that has a messed up header by default
                if x == 'Cubic':
                    table = xl.parse(usecols=[0,1,2], names=['Name', 'Composition', 'Group'], sheet_name=x, header=4, skip_blank_lines=True, skipinitialspace=True)
                else:
                    table = xl.parse(usecols=[0,1,2], names=['Name', 'Composition', 'Group'], sheet_name=x, skip_blank_lines=True, skipinitialspace=True)
                # Get rid of all lines with all NaN values (not including class labels)
                table.dropna(inplace=True, how="all", axis=1) # columns
                table.dropna(inplace=True, how="all", axis=0) # rows
                table.dropna(inplace=True, how="any", axis=0, thresh=2) # rows
                tables.append(table)
        results = pd.DataFrame(columns=tables[0].columns)
    for table in tables:
        results = pd.concat([results, table], sort=False)

    return results
