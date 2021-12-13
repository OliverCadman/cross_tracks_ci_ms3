document.addEventListener("DOMContentLoaded", function () {
  collectLikeButtons();
});

function collectLikeButtons() {
  let removeLikeButtons = document.getElementsByClassName("remove-like");

  for (let i = 0; i < removeLikeButtons.length; i++) {
    removeLikeButtons[i].addEventListener("click", removeLike);
  }
}

function removeLike(e) {
  e.preventDefault();
  $.ajax(this.href, {
    success: function (res) {
      if (res.liked_tracks.length === 0) {
        location.reload();
      } else {
        let removedTrack =
          e.target.parentElement.parentElement.parentElement.parentElement;
        removedTrack.remove();
      }
    },
  });
}
