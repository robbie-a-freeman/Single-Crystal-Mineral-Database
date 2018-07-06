function fillEntries(table) {
  console.log("being called");
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
  for (var i = 0; i < rows.length - 1; i++) {
    var tr = document.createElement("tr");
    var cells = rows[i].split("~*")
    for (var j = 0; j < 3; j++) {
      var link = document.createElement("a");
      link.setAttribute("href", "#");
      link.setAttribute("class", "undecorated");
      var td = document.createElement("td");
      node = document.createTextNode(cells[j]);
      link.appendChild(node);
      td.appendChild(link);
      tr.appendChild(td);
    }
    bigTable.appendChild(tr);
  }
  var element = document.getElementById("content");
  element.appendChild(bigTable);
}
