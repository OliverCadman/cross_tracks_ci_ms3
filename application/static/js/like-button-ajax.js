document.addEventListener("DOMContentLoaded", function () {
  collectLikeButtons();
});

// Collects all anchor tags with class 'like_track'
function collectLikeButtons() {
  let buttons = $(".like_track");

  for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click", addLikeAndUpdate);
  }
}

/* Use AJAX to call on add_like function in 
       application/tracks/views.py. Update the 
       relevant span with new number of likes */
function addLikeAndUpdate(e) {
  e.preventDefault();
  $.ajax(this.href, {
    success: function (res) {
        console.log(res)
        let numLikesContainer = e.target.parentElement.parentElement.parentElement.childNodes[4]
        if (res === 0) {
            numLikesContainer.innerHTML = ''
        } else {
            numLikesContainer.innerHTML = `${res}`
        }
    },
  });
}
