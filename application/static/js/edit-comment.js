/*
edit-comment.js

Toggles display of form with text input for user to edit their comments on tracks.

Functions:

    toggleForm():

    Toggles display and hiding of form when user clicks edit FontAwesome icon
    or 'Cancel' button, respectively.

    Comment text content and edit/delete icon buttons are replaced with text input
    when user clicks edit icon. They display when cancel button is clicked, or of 
    course when the submit button is clicked and page refreshes.

*/ 



$(document).ready(function(){
  let buttons = document.getElementsByTagName("button");

  /* Media query to check for mobile screen size
     Used to call seperate function to style input for mobile devices specifically.
     https://www.w3schools.com/howto/howto_js_media_queries.asp
     */

  let mobileScreen = window.matchMedia("(max-width: 414px)");

  for (buttonOne of buttons) {
    if (buttonOne.getAttribute("class").includes("edit-comment-btn")) {
      if (mobileScreen.matches) {
        buttonOne.param = "openCommentEdit";
        buttonOne.addEventListener("click", toggleFormMobile);
      } else {
        buttonOne.param = "openCommentEdit";
        buttonOne.addEventListener("click", toggleForm);
      }
    } else if (
      buttonOne.getAttribute("class").includes("cancel-comment-edit")
    ) {
      if (mobileScreen.matches) {
        buttonOne.param = "cancelCommentEdit";
        buttonOne.addEventListener("click", toggleFormMobile);
      } else {
        buttonOne.param = "cancelCommentEdit";
        buttonOne.addEventListener("click", toggleForm);
      }
    }
  }

  function toggleForm(e, x) {
    /* Handles display and hide of form and comment content/buttons for iPad device size and up */

    console.log("mobile click");
    let commentContent =
      e.target.parentElement.parentElement.parentElement.parentElement;

    let form =
      e.target.parentElement.parentElement.parentElement.parentElement
        .parentElement.children[1];

    if (e.currentTarget.param === "openCommentEdit") {
      form.style.display = "block";
      commentContent.style.display = "none";
    } else if (e.currentTarget.param === "cancelCommentEdit") {
      form = e.target.parentElement.parentElement;
      form.style.display = "none";

      commentContent =
        e.target.parentElement.parentElement.parentElement.children[0];
      commentContent.style.display = "flex";
    }
  }

  function toggleFormMobile(e) {
    /* Handles the display and hide of text input and comment content/buttons */

    let commentContent = e.target.parentElement.parentElement.parentElement;
    let form =
      e.target.parentElement.parentElement.parentElement.parentElement
        .children[1];

    if (e.currentTarget.param === "openCommentEdit") {
      form.style.display = "block";
      commentContent.style.display = "none";
    } else if (e.currentTarget.param === "cancelCommentEdit") {
      form = e.target.parentElement.parentElement;
      form.style.display = "none";

      commentContent =
        e.target.parentElement.parentElement.parentElement.children[0];
      commentContent.style.display = "flex";
    }
  }
})
