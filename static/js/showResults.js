/**
 * showResults.js
 * Formats the links of table rows using JQuery. Otherwise, the links don't look
 * look like proper links. Uses JQuery.
 *
 * @author  Robbie Freeman, robbie.a.freeman@gmail.com
 * @updated 2018-07-18
 * @link    results.html
 *
 */

// Called by results.html template. Builds the page based on a query from
// search.html given the string table of results and the list of desired
// properties of each result. Also takes in the list of columns, columns, as
// a string. rowNum is undefined unless it's from a specific mineral query
function fillEntries(table, properties, columns, rowNum) {
  // if a rowNum is passed in, it's an individual mineral page. Otherwise, it's
  // a dynamic search result page
  var isSingleEntry = !(typeof rowNum == 'undefined');
  columns = columns.split(", ");
  var rows = table.split("\\");
  var h6 = document.createElement("h6");
  var resultAmount = rows.length - 1; // There's an extra row in the table due to invisible characters
  var content = document.getElementById("content");
  if (!isSingleEntry) {
    var resultText;
    if (resultAmount == 1) {
      resultText = document.createTextNode("1 result found");
    } else {
      resultText = document.createTextNode(resultAmount + " results found");
    }
    h6.appendChild(resultText);
    content.appendChild(h6);
  } else {
    title = document.getElementById("results-title");
    var cells = rows[0].split("~*");
    title.innerHTML = cells[0] + " Information";
  }

  br = document.createElement("br");
  content.appendChild(br);
  for (var i = 0; i < resultAmount; i++) {
    var cells = rows[i].split("~*");
    displayMineral(cells, properties, columns);
    if (!isSingleEntry) {
      var hr = document.createElement("hr");
      content.appendChild(hr);
      br = document.createElement("br");
      content.appendChild(br);
    }
  }
}

// Displays a mineral from a row of cells, which is in array form, and from the
// list of properties to display. Also takes in list of columns to insert
function displayMineral(row, properties, columns) {
  // Set up header content
  var node = document.createTextNode("Mineral: " + row[0] + " (" + row[1] + ")");
  var h3 = document.createElement("h3");
  h3.appendChild(node);
  // h3.setAttribute("data-href", 'search/' + rowNum); TODO: attach mineral links to headers of mineral data chunks
  var content = document.getElementById("content");
  content.appendChild(h3);

  // Basic information that always shows up
  node = document.createTextNode("Basic information");
  var h5 = document.createElement("h5");
  h5.appendChild(node);
  content.appendChild(h5);
  node = document.createTextNode("Group: " + row[2]);
  var p = document.createElement("p");
  p.appendChild(node);
  content.appendChild(p);
  node = document.createTextNode("Structure/SG: " + row[3]);
  p = document.createElement("p");
  p.appendChild(node);
  content.appendChild(p);
  node = document.createTextNode("C1: " + row[4]);
  p = document.createElement("p");
  p.appendChild(node);
  content.appendChild(p);
  node = document.createTextNode("NS: " + row[5]);
  p = document.createElement("p");
  p.appendChild(node);
  content.appendChild(p);
  var cubed = document.createElement("sup");
  node = document.createTextNode("3");
  cubed.appendChild(node);
  var str1 = "Density (g/cm";
  node = document.createTextNode(str1);
  var str2 = "): " + row[6];
  node2 = document.createTextNode(str2);
  p = document.createElement("p");
  p.appendChild(node);
  p.appendChild(cubed);
  p.appendChild(node2);
  content.appendChild(p);

  // If property is included, build the table for elastic constants
  if (properties.includes("aem") || properties.includes("all_cats")) {
    h5 = document.createElement("h5");
    h5.innerHTML = "Adiabatic elastic moduli (GPa)";
    content.appendChild(h5);
    var labels = ["C<sub>11</sub>", "C<sub>44</sub>", "C<sub>12</sub>"];
    var data = row;
    var indices = [locateIndexOf("&#39;11&#39;", columns),
                   locateIndexOf("&#39;44&#39;", columns),
                   locateIndexOf("&#39;12&#39;", columns)];
    buildTable(labels, data, indices);
  }
  // If property is included, build the tables for other elastic constant data
  if (properties.includes("ympr") || properties.includes("hsb") ||
      properties.includes("vrb") || properties.includes("vrh") ||
      properties.includes("am") || properties.includes("all_cats")) {
        h5 = document.createElement("h5");
        h5.innerHTML = "Aggregate adiabatic elastic moduli (GPa)";
        content.appendChild(h5);
  }

  if (properties.includes("vrh") || properties.includes("am") || properties.includes("all_cats")) {
    var h6 = document.createElement("h6");
    h6.innerHTML = "Voigt-Reuss-Hill averages (GPa)";
    content.appendChild(h6);
    var labels = ["K", "G", "K/G"];
    var data = row;
    var indices = [locateIndexOf("&#39;K&#39;", columns),
                   locateIndexOf("&#39;G&#39;", columns),
                   locateIndexOf("&#39;K/G&#39;", columns)];
    buildTable(labels, data, indices);
  }

  if (properties.includes("vrb") || properties.includes("am") || properties.includes("all_cats")) {
    var h6 = document.createElement("h6");
    h6.innerHTML = "Voigt, Reuss bounds on shear modulus (GPa)";
    content.appendChild(h6);
    labels = ["G<sub>R</sub>", "G<sub>V</sub>"];
    data = row;
    indices = [locateIndexOf("&#39;GR&#39;", columns),
               locateIndexOf("&#39;GV&#39;", columns)];
    buildTable(labels, data, indices);
  }
  if (properties.includes("hsb") || properties.includes("am") || properties.includes("all_cats")) {
    var h6 = document.createElement("h6");
    h6.innerHTML = "Hashin-Shtrikman bounds on shear modulus (GPa)";
    content.appendChild(h6);
    labels = ["G<sub>HS1</sub>", "G<sub>HS2</sub>", "G<sub>HSA</sub>"];
    data = row;
    indices = [locateIndexOf("&#39;GHS1&#39;", columns),
               locateIndexOf("&#39;GHS2&#39;", columns),
               locateIndexOf("&#39;GHSA&#39;", columns)];
    buildTable(labels, data, indices);
  }
  if (properties.includes("ympr") || properties.includes("am") || properties.includes("all_cats")) {
    var h6 = document.createElement("h6");
    h6.innerHTML = "Aggregate Young’s modulus and Poisson’s ratio";
    content.appendChild(h6);
    labels = ["nVRH", "EVRH"];
    data = row;
    indices = [locateIndexOf("&#39;nVRH&#39;", columns),
               locateIndexOf("&#39;EVRH&#39;", columns)];
    buildTable(labels, data, indices);
  }
  // If property is included, build the tables for sound velocity data
  if (properties.includes("sv") || properties.includes("all_cats")) {
    h5 = document.createElement("h5");
    h5.innerHTML = "Sound velocities (km/s)";
    content.appendChild(h5);
    var labels = ["V<sub>P</sub>", "V<sub>B</sub>", "V<sub>S</sub>"];
    var data = row;
    var indices = [locateIndexOf("&#39;VP&#39;", columns),
                   locateIndexOf("&#39;VB&#39;", columns),
                   locateIndexOf("&#39;VS&#39;", columns)];
    buildTable(labels, data, indices);
  }
  // If property is included, build the tables for sound velocity ratio data
  if (properties.includes("svr") || properties.includes("all_cats")) {
    h5 = document.createElement("h5");
    h5.innerHTML = "Sound velocity ratio";
    content.appendChild(h5);
    var labels = ["V<sub>P</sub>/V<sub>S</sub>"];
    var data = row;
    var indices = [locateIndexOf("&#39;VP/VS&#39;", columns)];
    buildTable(labels, data, indices);
  }
  // If property is included, build the tables for normalized elastic moduli
  if (properties.includes("nm") || properties.includes("all_cats")) {
    h5 = document.createElement("h5");
    h5.innerHTML = "Normalized elastic moduli";
    content.appendChild(h5);
    var labels = ["C<sub>44</sub>/C<sub>11</sub>", "C<sub>12</sub>/C<sub>11</sub>"];
    var data = row;
    var indices = [locateIndexOf("&#39;C44/C11&#39;", columns),
                  locateIndexOf("&#39;C12/C11&#39;", columns)];
    buildTable(labels, data, indices);
  }
  // If property is included, build the tables for anisotropy factors
  if (properties.includes("af") || properties.includes("all_cats")) {
    h5 = document.createElement("h5");
    h5.innerHTML = "Anisotropy factors";
    content.appendChild(h5);
    var labels = ["A<sub>Z</sub>", "A<sub>G</sub>", "A<sub>U</sub>", "A<sub>L</sub>"];
    var data = row;
    var indices = [locateIndexOf("&#39;AZ&#39;", columns),
                   locateIndexOf("&#39;AG&#39;", columns),
                   locateIndexOf("&#39;AU&#39;", columns),
                   locateIndexOf("&#39;AL&#39;", columns)];
    buildTable(labels, data, indices);
  }
  // If property is included, build the tables for elastic compliances
  if (properties.includes("ec") || properties.includes("all_cats")) {
    h5 = document.createElement("h5");
    h5.innerHTML = "Adiabatic elastic compliances (GPa<sup>-1</sup>)";
    content.appendChild(h5);
    var labels = ["S<sub>11</sub>", "S<sub>44</sub>", "S<sub>12</sub>"];
    var data = row;
    console.log(columns);
    var indices = [locateIndexOf("&#39;S11&#39;", columns),
                   locateIndexOf("&#39;S44&#39;", columns),
                   locateIndexOf("&#39;S12&#39;", columns)];
    buildTable(labels, data, indices);
  }
  // If property is included, build the tables for Poisson’s ratio
  if (properties.includes("pre") || properties.includes("all_cats")) {
    h5 = document.createElement("h5");
    h5.innerHTML = "Extrema of Poisson’s ratio";
    content.appendChild(h5);
    var labels = ["n_110", "n_001"];
    var data = row;
    var indices = [locateIndexOf("&#39;n_110&#39;", columns),
                   locateIndexOf("&#39;n_001&#39;", columns)];
    buildTable(labels, data, indices);
  }

  // Create space between minerals and between the last mineral and the end of
  // the page
  br = document.createElement("br");
  content.appendChild(br);
}

// Build a table with HTML elements with the given column labels and data as the
// rows
function buildTable(labels, data, indices) {
  var table = document.createElement("table");
  table.setAttribute("align", "center");

  var th; // add in the table headers
  var name;
  for (var i = 0; i < labels.length; i++) {
    th = document.createElement("th");
    th.innerHTML = labels[i];
    table.appendChild(th);
  }

  var tr; // append the rest of the data below
  var td;
  var name;
  tr = document.createElement("tr");
  for (var i = 0; i < indices.length; i++) {
    td = document.createElement("td");
    name = document.createTextNode(data[indices[i]]);
    td.appendChild(name);
    tr.appendChild(td);
  }
  table.appendChild(tr);
  var content = document.getElementById("content");
  content.appendChild(table);
}

// Takes in a string and finds it in the array that is passed from fetch.py.
// Returns an int representing the index, -1 if not found.
function locateIndexOf(string, array) {
  // if the brackets remain from the python array remnants, find the string anyway
  var index = array.indexOf(string);
  if (index == -1) {
    endString = string + ']';
    index = array.indexOf(endString);
    if (index == -1) {
      beginningString = '[' + string;
      index = array.indexOf(beginningString);
    }
  }

  console.log(index);
  return index;
}
