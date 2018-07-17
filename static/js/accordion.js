/**
 * checkboxes.js
 * Controls the accordions in search.html. Adapted slightly.
 * source: https://www.w3schools.com/howto/howto_js_accordion.asp
 *
 * @author  Robbie Freeman, robbie.a.freeman@gmail.com
 * @updated 2018-07-17
 * @link    search.html
 *
 */

var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function(event) {
      event.preventDefault();
      /* Toggle between adding and removing the "active" class,
      to highlight the button that controls the panel */
      this.classList.toggle("active");

      /* Toggle between hiding and showing the active panel */
      var structures = this.nextElementSibling.nextElementSibling; /* skip <br> */
      if (structures.style.display === "block") {
        structures.style.display = "none";
      } else {
        structures.style.display = "block";
      }
    });
}
