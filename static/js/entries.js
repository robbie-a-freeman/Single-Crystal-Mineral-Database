function fillEntries(table) {
  console.log("being called");
  var bigTable = document.createElement("table");
  bigTable.setAttribute("align", "center");
  // for each line in the string, make a table row and fill it with entries
  // split by backslashes
  var rows = table.split("\\");
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
  var rowNum = 0;
  for (var i = 0; i < rows.length; i++) {
    var tr = document.createElement("tr");
    var cells = rows[i].split("~*")
    for (var j = 0; j < cells.length - 1; j++) {
      var td = document.createElement("td");
      node = document.createTextNode(cells[j]);
      td.appendChild(node);
      tr.appendChild(td);
    }
    tr.setAttribute("data-href", 'search/' + rowNum);
    bigTable.appendChild(tr);
    rowNum++;
  }
  var element = document.getElementById("content");
  element.appendChild(bigTable);
}
//var tableHead = document.createElement("th");
