/**
 * checkboxes.js
 * Allows for heirarchical checkboxes. There's probably a much cleaner and more
 * flexible solution in place, but this is of my own design. In a given page,
 * a checkbox can have a parent with an id='x' (for example). To identify that
 * the checkbox is the child, it must have class='x'. Therefore, it's possible
 * for checkboxes to have multiple different parents, but a checkbox can only be
 * one category of parent. This function checks the checkboxes for every change.
 *
 * @author  Robbie Freeman, robbie.a.freeman@gmail.com
 * @updated 2018-07-17
 * @link    search.html
 *
 */

// Controls the control flow of the script.
var evalCheckboxes = function () {
  /* select all checked boxes if not done already */
  /* checks if any children need to be checked */
  if ($(this).prop('checked') && $(this).prop('id') !== "") {
    //$('.' + $(this).prop('id')).prop('checked', true);
    checkDown($(this));
  } else if ($(this).prop('id') !== '') {
    //$('.' + $(this).prop('id')).prop('checked', false);
    checkDown($(this));
  }

  /* Check or uncheck the parent boxes as appropriate */
  checkUp($(this));
}

// Checks the checkboxes below the given checkbox recursively
function checkDown(checkbox) {
  var children = document.getElementsByClassName(checkbox.prop('id'));
  if (checkbox.prop('checked') && checkbox.prop('id') !== '') {
    for (var i = 0; i < children.length; i++) {
      children[i].checked = true;
      if (children[i].id !== '') {
        checkDown($(children[i]));
      }
    }
  } else if ($(checkbox).prop('id') !== '') {
    for (var i = 0; i < children.length; i++) {
      children[i].checked = false;
      if (children[i].id !== '') {
        checkDown($(children[i]));
      }
    }
  }
}

// Checks the checkboxes above the given checkbox recursively
function checkUp(checkbox) {
  var all = document.getElementsByClassName(checkbox.prop("class"));
  var allChecked = true;

  for (var i=0; i < all.length; i++) {
    if (all[i].checked != true) {
      document.getElementById(checkbox.prop("class")).checked = false;
      if (checkbox.prop('class') !== '') {
        checkUp($('#' + checkbox.prop('class')));
      }
      allChecked = false;
      break;
    }
  }
  if (allChecked == true && all.length > 0) {
    document.getElementById(checkbox.prop("class")).checked = true;
    if (checkbox.prop('class') !== '') {
      checkUp($('#' + checkbox.prop('class')));
    }
  }
}

// Actually calls the script on any new inputs to the form
$('input').change(evalCheckboxes);
