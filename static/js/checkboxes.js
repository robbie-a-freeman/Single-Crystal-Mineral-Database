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

function checkUp(checkbox) {
  var all = document.getElementsByClassName(checkbox.prop("class"));
  var allChecked = true;
  console.log(all);

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

$('input').change(evalCheckboxes);
