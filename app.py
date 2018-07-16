from flask import Flask
from flask import render_template
from flask import request
from flask import json
from flask import abort
from flask import redirect
from flask import url_for
import sys
sys.path.insert(0, 'static/py')
import allEntries
import fetch

app = Flask(__name__)

@app.route('/changelog')
def changelog():
    return render_template('changelog.html')

@app.route('/databases')
def databases():
    return render_template('databases.html')

@app.route('/definitions')
def definitions():
    return render_template('definitions.html')

@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

@app.route('/entries')
def entries():
    table = allEntries.main()
    return render_template('entries.html', table=table)

@app.route('/links')
def links():
    return render_template('links.html')

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST': # if args are passed
        return searchResults(request.form)
    return render_template('search.html')

def searchResults(query_params):
    results = fetch.search(query_params) # Has to be called first
    properties = fetch.getSelectedProperties()
    columns = fetch.getColumnNames()
    return render_template('results.html', table = results, properties = properties, columns = columns)

@app.route('/search/<rowNum>')
def specificResult(rowNum):
    print(rowNum)
    results = fetch.getMineral(rowNum) # Has to be called first
    properties = fetch.getSelectedProperties()
    columns = fetch.getColumnNames()
    return render_template('results.html', table = results, properties = properties, columns = columns)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run()

def processRequest(request) :
    table = allEntries.main()
    return table
