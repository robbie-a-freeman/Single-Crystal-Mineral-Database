/**
 * entries.js
 * Reads in the entry results from fetch.py (funneled through results.html) and
 * creates a table with the name, composition, and group/structure of each
 * mineral in the database.
 *
 * @author  Robbie Freeman, robbie.a.freeman@gmail.com
 * @updated 2019-04-23
 * @link    entries.html
 *
 */

// Called by entries.html. Creates the table mineral by mineral with the table,
// really a formatted string, as the sole parameter.

// Note: table is a basically a 5 column object. First 4 columns are the Name,
// Composition, and Structure/SG of the mineral, but the last column is \\\ because
// JS does not like taking in multi-line strings, so that is how the language
// takes in the string.
function fillEntries(table) {
  var bigTable = document.createElement("table");
  bigTable.setAttribute("align", "center");
  // for each line in the string, make a table row and fill it with entries
  // split by backslashes
  var rows = table.split("\\");
  // create heads of the table
  var thead = document.createElement("thead");
  var trh = document.createElement("tr");
  var th = document.createElement("th");
  var node = document.createTextNode("Name");
  th.appendChild(node);
  trh.appendChild(th);
  th = document.createElement("th");
  node = document.createTextNode("Composition");
  th.appendChild(node);
  trh.appendChild(th);
  th = document.createElement("th");
  node = document.createTextNode("Group");
  th.appendChild(node);
  trh.appendChild(th);
  thead.appendChild(trh);
  bigTable.appendChild(thead);

  // I don't know how this gets in here, but take it out
  rows[0] = rows[0].replace('b&#39;', '');

  var tbody = document.createElement("tbody");
  // generates row of each mineral
  for (var i = 0; i < rows.length; i++) {
    var tr = document.createElement("tr");
    var cells = rows[i].split("~*")
    for (var j = 0; j < cells.length - 2; j++) {
      var td = document.createElement("td");
      if (j == 0) { // if in the name column, convert the abbrieviations
        cells[j] = replaceAbbrievs(cells[j]); // from replaceAbbrievs.js
      }
      if (cells[j] == "nan") {
        cells[j] = "N/A"
      }
      node = document.createTextNode(cells[j]);
      td.appendChild(node);
      tr.appendChild(td);
    }
    // individual mineral links. rowNum is the row in the pandas dataframe of the
    // mineral
    var entryNum = cells[3];
    tr.setAttribute("data-href", 'search/' + entryNum);
    tbody.appendChild(tr);
  }
  bigTable.appendChild(tbody);
  var element = document.getElementById("content");
  element.appendChild(bigTable);
  bigTable.setAttribute("class", "sortable");
}
