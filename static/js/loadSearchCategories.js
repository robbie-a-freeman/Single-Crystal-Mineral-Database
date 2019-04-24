/**
 * loadSearchCategories.js
 * Takes in the searching categories from the server and formats the checkboxes
 * accordingly
 *
 * @author  Robbie Freeman, robbie.a.freeman@gmail.com
 * @updated 2019-04-24
 * @link    search.html
 *
 */

function generateCheckboxes(mineralTypes) {

  // clean up the data passed in from the server
  mineralTypes = mineralTypes.split(']');

  for (var i = 0; i < mineralTypes.length; i++) {
    var mineralTypeName = mineralTypes[i].split('[')[0];
    if (mineralTypeName == "") {
      break;
    }
    var categories = mineralTypes[i].split('[')[1].split('),');
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

    // for each mineralTypeName

    //console.log(mineralTypeName);
    generateCheckboxFamily("all_minerals", mineralTypeName, []);
    categories.forEach(function(cat, index) {
      var cats = cat.split(',');
      //if (minClass != cats[0]) {
      //generateGroupCheckbox(minClass, minStructList);
      //var input = document.createElement("div");
      //input.setAttribute("id", "sub_category_" + i);
      generateCheckboxFamily(mineralTypeName, cats[0]);
      //minClass = cats[0];
      //minStructList = [cats[1]];
      //} else {
      //  minStructList.push(cats[1]); }
    });
    // generateGroupCheckbox(minClass, minStructList); // for the last one
    generateCheckboxFamily(mineralTypeName, minClass, minStructList);
  }

}

// Takes in the name of a supercheckbox and its sublist of subcheckboxes. creates
// a checkbox that acts as a selectall for the sublist. Calls generateSingleCheckbox()
// to create the sublist's checkboxes
function generateCheckboxFamily(parent, name) {

  // check for dupes
  if (document.getElementById(name.toLowerCase()) != null) {
    return null;
  }

  // heirarchy is grandparent div > parentCheckbox and parentDiv > input (new checkbox)
  var isFirstInFamily = false;
  // create/retrieve the parentDiv
  var parentDiv = document.getElementById(parent.toLowerCase() + "_children");
  if (parentDiv == null || !$(parentDiv).length) {
    isFirstInFamily = true;
    parentDiv = document.createElement("div");
    parentDiv.setAttribute("id", parent.toLowerCase() + "_children");
    parentDiv.setAttribute("class", "sub_categories");
    parentDiv.setAttribute("style", "display: none;");
  }

  // create and insert new checkbox and its data
  var input = document.createElement("input");
  input.setAttribute("id", name.toLowerCase());
  input.setAttribute("class", parent.toLowerCase());
  input.setAttribute("type", "checkbox");
  input.setAttribute("name", name + "_all");
  input.setAttribute("value", name + "_all");

  var inputDiv = document.createElement("div");
  inputDiv.setAttribute("id", name.toLowerCase() + "_box_div");
  var node = document.createTextNode(" " + name);
  inputDiv.appendChild(input);
  inputDiv.appendChild(node);
  parentDiv.appendChild(inputDiv);

  var grandparentDiv = (document.getElementById(parent.toLowerCase())).parentElement;

  // if the first checkbox in parentDiv, create accordion button
  if (isFirstInFamily) {
    var button = document.createElement("button");
    button.setAttribute("class", "accordion");
    button.innerHTML = " + ";
    grandparentDiv.appendChild(button);
  }
  grandparentDiv.appendChild(parentDiv);
  return input;
}
