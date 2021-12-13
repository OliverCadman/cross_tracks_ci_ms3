/* JavaScript hooked up to templates/browse-tracks.html
Loops through anchor tags with href '{{url_for('tracks.like_track)}}'
and uses AJAX to call the like_track function, and update the DOM 
asynchronously */

document.addEventListener("DOMContentLoaded", function () {
  collectLikeButtons();
});

// Collects all anchor tags with class 'like_track'
function collectLikeButtons() {
  let buttonsMed = $(".like_track_med");

  for (let i = 0; i < buttonsMed.length; i++) {
    buttonsMed[i].addEventListener("click", addRemoveLikeMed);
  }

  let buttonsMob = $(".like_track_mob");

  for (let i = 0; i < buttonsMob.length; i++) {
    buttonsMob[i].addEventListener("click", addRemoveLikeMob);
  }
}

/* Use AJAX to call on add_like function in 
       application/tracks/views.py. Update the 
       relevant span with new number of likes */
function addRemoveLikeMed(e) {
  e.preventDefault();
  $.ajax(this.href, {
    success: function (res) {
      // Update the DOM element displaying number of likes
      let numLikesContainer =
        e.target.parentElement.parentElement.parentElement.childNodes[4];

      if (res.num_of_likes === 0) {
        numLikesContainer.innerHTML = "";
      } else {
        numLikesContainer.innerHTML = `${res.num_of_likes}`;
      }

      let currentUser = res.username;
      let listOfLikes = res.likes_list;
      let likeIcon = e.target.parentElement.children[0];

      /* Replace FontAwesome star icon outline with 
        filled star if track is liked, and vice versa */
      if (listOfLikes.includes(currentUser)) {
        likeIcon.classList.remove("far", "fa-star");
        likeIcon.classList.add("fas", "fa-star");
      } else {
        likeIcon.classList.remove("fas", "fa-star");
        likeIcon.classList.add("far", "fa-star");
      }
    },
  });
}

function addRemoveLikeMob(e) {
  e.preventDefault();

  $.ajax(this.href, {
    success: function (res) {
      let numLikesContainer =
        e.target.parentElement.parentElement.parentElement.children[3];

      if (res.num_of_likes === 0) {
        numLikesContainer.innerHTML = "";
      } else {
        numLikesContainer.innerHTML = `${res.num_of_likes}`;
      }

      let currentUser = res.username;
      let listOfLikes = res.likes_list;
      let likeIcon =
        e.target.parentElement.parentElement.parentElement.children[2]
          .children[0].children[0];

      if (listOfLikes.includes(currentUser)) {
        likeIcon.classList.remove("far", "fa-star");
        likeIcon.classList.add("fas", "fa-star");
      } else {
        likeIcon.classList.remove("fas", "fa-star");
        likeIcon.classList.add("far", "fa-star");
      }
    },
  });
}
