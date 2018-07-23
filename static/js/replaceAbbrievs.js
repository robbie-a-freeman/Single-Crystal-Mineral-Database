/**
 * replaceAbbrievs.js
 * Holds a function that replaces the abbreivatiations that are contained in the
 * database in certain places, namely the Name column where the mineral is
 * identified.
 *
 * Converts x into y where x | y:
 * Prp | Pyrope
 * Alm | Almandine
 * Grs | Grossular
 * Spr | Spessartine
 * Uv | Uvarovite
 * Adr | Andradite
 * Hgr | Hydrogrossular
 * Maj | Majorite
 *
 * Assumes titles of the format One-Two-Three, title case, parts separated by
 * dashes.
 *
 * @author  Robbie Freeman, robbie.a.freeman@gmail.com
 * @updated 2018-07-22
 * @link    results.html, entries.html
 *
 */

/* Takes in a string, breaks it up by -, and scans each part for the abbreivs
   defined above */
function replaceAbbrievs(string) {
  stringSubparts = string.split("-");
  stringSubparts.forEach(function(word, index) {
    if (word == "Prp") {
      word = 'Pyrope';
      stringSubparts[index] = word;
    }
    if (word == "Alm") {
      word = 'Almandine';
      stringSubparts[index] = word;
    }
    if (word == "Grs") {
      word = 'Grossular';
      stringSubparts[index] = word;
    }
    if (word == "Spr") {
      word = 'Spessartine';
      stringSubparts[index] = word;
    }
    if (word == "Uv") {
      word = 'Uvarovite';
      stringSubparts[index] = word;
    }
    if (word == "Adr") {
      word = 'Andradite';
      stringSubparts[index] = word;
    }
    if (word == "Hgr") {
      word = 'Hydrogrossular';
      stringSubparts[index] = word;
    }
    if (word == "Maj") {
      word = 'Majorite';
      stringSubparts[index] = word;
    }
  });
  finalString = "";
  stringSubparts.forEach(function(word, index) {
    if (index == stringSubparts.length - 1) {
      finalString = finalString + word;
    } else {
      finalString = finalString + word + "-";
    }
  });
  return finalString;
}
