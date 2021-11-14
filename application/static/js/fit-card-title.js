/* 
Alters the font size of track names which are too long to fit
onto one line. Uses the getBoundingClientRect() API to query
for the card title element's width.
*/
document.addEventListener('DOMContentLoaded', function() {
    let elem = document.getElementsByClassName("card-title");
    for (let i = 0; i < elem.length; i++) {
      let rect = elem[i].getBoundingClientRect();

      if (rect.width >= 250) {
        elem[i].style.fontSize = "1.4rem";
      }
    }
})

