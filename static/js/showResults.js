function fillEntries(table) {
  var bigTable = document.createElement("table");
  bigTable.setAttribute("align", "center");
  // for each line in the string, make a table row and fill it with entries
  // split by backslashes
  var rows = table.split("\\");
  console.log(rows.length);
  var th = document.createElement("th");
  var node = document.createTextNode("Name");
  th.appendChild(node);
  bigTable.appendChild(th);
  th = document.createElement("th");
  node = document.createTextNode("Composition");
  th.appendChild(node);
  bigTable.appendChild(th);
  th = document.createElement("th");
  node = document.createTextNode("Group");
  th.appendChild(node);
  bigTable.appendChild(th);
  for (var i = 0; i < rows.length - 1; i++) { // Skip the last column, which are
    var tr = document.createElement("tr");    // the backslashes to make the js
    var cells = rows[i].split("~*")           // read the multiline string.
    for (var j = 0; j < 3; j++) {             // Also, parse the cells
      var td = document.createElement("td");
      node = document.createTextNode(cells[j]);
      td.appendChild(node);
      tr.appendChild(td);
    }
    tr.setAttribute("data-href", "#");
    bigTable.appendChild(tr);
  }
  var element = document.getElementById("content");
  element.appendChild(bigTable);
}
