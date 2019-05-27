/**
 * checkboxes.js
 * Controls the accordions in search.html. Adapted slightly.
 * source: https://www.w3schools.com/howto/howto_js_accordion.asp
 *
 * @author  Robbie Freeman, robbie.a.freeman@gmail.com
 * @updated 2019-05-25
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
      var sublist = document.getElementById(this.previousElementSibling.id + "-children"); /* skip <br> */
      console.log(this);
      console.log(this.previousElementSibling.id);
      if (sublist.style.display === "block") {
        sublist.style.display = "none";
      } else {
        sublist.style.display = "block";
      }
    });
}
