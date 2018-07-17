/**
 * tableLinks.js
 * Formats the links of table rows using JQuery. Otherwise, the links don't look
 * look like proper links. Uses JQuery.
 *
 * @author  Robbie Freeman, robbie.a.freeman@gmail.com
 * @updated 2018-07-17
 * @link    entries.html
 *
 */

// Creates the link at each table row
$('*[data-href]').on("click",function(){
  window.location = $(this).data('href');
  return false;
});
// Turns mouse into pointer (on hover)
$('*[data-href]').css('cursor', 'pointer');
