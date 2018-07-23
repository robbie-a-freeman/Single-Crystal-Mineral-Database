"""Controls the web server for the entire site with a Flask framework. Assumes
that the main app is app.py. Contains links to the rest of the site, and it
handles non-static downloads.
"""

from flask import Flask
from flask import render_template
from flask import request
from flask import json
from flask import abort
from flask import redirect
from flask import url_for
from flask import send_file
import os
import sys
sys.path.insert(0, 'static/py')
import fetch
import allEntries

app = Flask(__name__)

__author__ = "Robbie Freeman"
__credits__ = ["Thomas Duffy"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

resultsTable = None

# loads the changelog
@app.route('/changelog')
def changelog():
    return render_template('changelog.html')

# loads the page of related databases
@app.route('/databases')
def databases():
    return render_template('databases.html')

# loads the page of more complete search.html definitions
@app.route('/definitions')
def definitions():
    return render_template('definitions.html')

# loads the CSV file of appropriate results in results.html
@app.route('/downloadCSVResults')
def downloadCSVResults():
    global resultsTable
    if resultsTable is None:
        print("NONE")
        return render_template('results.html', table = None, properties = None, columns = None)
    createCSVSheet(resultsTable)
    return send_file('Single_Crystal_Mineral_Database_Results.csv')

# loads the Excel file of appropriate results in results.html
@app.route('/downloadExcelResults')
def downloadExcelResults():
    global resultsTable
    if resultsTable is None:
        print("NONE")
        return render_template('results.html', table = None, properties = None, columns = None)
    createExcelSheet(resultsTable)
    return send_file('Single_Crystal_Mineral_Database_Results.xlsx')

# loads the downloads page
@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

# generates and loads the entire database quickly
@app.route('/entries')
def entries():
    if not os.path.isfile('static/text/all.txt'):
        allEntries()
    file = open('static/text/all.txt', 'r')
    table = file.read()
    table = table[:-1]
    return render_template('entries.html', table=table)

# loads the home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

# loads list of related links of other projects
@app.route('/links')
def links():
    return render_template('links.html')

# loads the search page, and also reads in post requests from searchs on that
# page.
@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST': # if args are passed
        return searchResults(request.form)
    return render_template('search.html')

# finds the results using fetch.py of a search query from search.html. Alters
# the global table of results and grabs variables for use in the showResults.js
# file. Returns results.html page
def searchResults(query_params):
    results = fetch.search(query_params) # Has to be called first
    properties = fetch.getSelectedProperties()
    columns = fetch.getColumnNames()
    global resultsTable
    resultsTable = fetch.getResultsTable()
    return render_template('results.html', table = results, properties = properties, columns = columns)

# finds specific results, namely a single mineral. Used for links in entries.html
# and in the results.html #TODO. Returns single-mineral version of results.html
@app.route('/search/<rowNum>')
def specificResult(rowNum):
    print(rowNum)
    results = fetch.getMineral(rowNum) # Has to be called first
    properties = fetch.getSelectedProperties()
    columns = fetch.getColumnNames()
    global resultsTable
    resultsTable = fetch.getResultsTable()
    return render_template('results.html', table = results, properties = properties, columns = columns, rowNum = rowNum)

# basic 404 page. Hopefully isn't called all that often
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# calls the app so it can run
if __name__ == "__main__":
    app.run()

# converts pandas table into excel sheet for download. Returns nothing
def createExcelSheet(table) :
    # format the table appropriately
    print(table)
    table.drop(['\\\\\\'], axis=1, inplace=True)
    print(table.columns)
    # make the excel writer
    import pandas as pd
    writer = pd.ExcelWriter('Single_Crystal_Mineral_Database_Results.xlsx')
    table.to_excel(writer,'Search Results', index=False)
    ref1 = pd.read_excel('static/downloads/single-crystal_db.xlsx', sheetname='Refs and Notes')
    ref1.to_excel(writer,'Refs and Notes', index=False, header=False)
    ref2 = pd.read_excel('static/downloads/single-crystal_db.xlsx', sheetname='Key and Abbreviations')
    ref2.to_excel(writer,'Key and Abbreviations', index=False, header=False)
    writer.save()

# converts pandas table into CSV file for download. Returns nothing
def createCSVSheet(table) :
    # format the table appropriately

    # convert to csv
    import pandas as pd
    table.to_csv('Single_Crystal_Mineral_Database_Results.csv')
