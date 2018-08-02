/**
 * loadSearchCategories.js
 * Takes in the searching categories from the server and formats the checkboxes
 * accordingly
 *
 * @author  Robbie Freeman, robbie.a.freeman@gmail.com
 * @updated 2018-07-24
 * @link    search.html
 *
 */

function generateCheckboxes(categories) {
  categories = categories.split('),');
  // clean up the tuples passed in from the server
  categories.forEach(function(cat, index) {
    cat = cat.replace(/&#39;/g, '');
    cat = cat.replace(/\(/g, '');
    cat = cat.replace(/\)/g, '');
    cat = cat.replace(/\[/g, '');
    cat = cat.replace(/\]/g, '');
    cat = cat.replace(/ /g, '');
    cat = cat.replace(/&amp;#160;/g, ' ');
    if (cat.split(',')[0] != '' && cat.split(',')[1] != '') {
      categories[index] = cat;
    }
  });
  // store each group of structures as an array of their shared parent mineral class
  var minClass = categories[0].split(',')[0];
  var minStructList = [];
  categories.forEach(function(cat, index) {
    var cats = cat.split(',');
    if (minClass != cats[0]) {
      generateGroupCheckbox(minClass, minStructList);
      minClass = cats[0];
      minStructList = [cats[1]];
    } else {
      minStructList.push(cats[1]);
    }
  });
    generateGroupCheckbox(minClass, minStructList); // for the last one
}

// Takes in the name of a mineral class group and its sublist of structures. creates
// a checkbox that acts as a selectall for the sublist. Calls generateStructureCheckbox()
// to create the sublist's checkboxes
function generateGroupCheckbox(group, structures) {
  var sub_categories = document.getElementById("sub_categories");
  var input = document.createElement("input");
  input.setAttribute("id", group.toLowerCase());
  input.setAttribute("class", "all_minerals");
  input.setAttribute("type", "checkbox");
  input.setAttribute("name", group + "_all");
  input.setAttribute("value", group + "_all");
  sub_categories.appendChild(input);
  node = document.createTextNode(" " + group);
  sub_categories.appendChild(node);
  var button = document.createElement("button");
  button.setAttribute("class", "accordion");
  button.innerHTML = " + ";
  sub_categories.appendChild(button);
  var br = document.createElement("br");
  sub_categories.appendChild(br);

  var structuresDiv = document.createElement("div");
  structuresDiv.setAttribute("class", "structures");
  structures.forEach(function(structure) {
    structuresDiv.appendChild(generateStructureCheckbox(group, structure));
    structuresDiv.appendChild(document.createTextNode(" " + structure));
    br = document.createElement("br");
    structuresDiv.appendChild(br);
  });

  sub_categories.appendChild(structuresDiv);
}

// Takes in name of mineral class and the structure. Makes the checkbox and makes it a
// child of the mineral class checkbox
function generateStructureCheckbox(group, structure) {
  var input = document.createElement("input");
  input.setAttribute("class", group.toLowerCase());
  input.setAttribute("type", "checkbox");
  input.setAttribute("name", group + "_" + structure);
  input.setAttribute("value", group + "_" + structure);
  return input;
}
