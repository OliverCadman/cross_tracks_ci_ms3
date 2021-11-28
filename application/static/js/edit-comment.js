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

    let buttons = document.getElementsByTagName("button")

    for (buttonOne of buttons) {
        if (buttonOne.getAttribute('class').includes("edit-comment-btn")) {
            buttonOne.param = "openCommentEdit"
            buttonOne.addEventListener("click", toggleForm)
        } else if (buttonOne.getAttribute('class').includes("cancel-comment-edit")) {
            buttonOne.param = "cancelCommentEdit"
            buttonOne.addEventListener("click", toggleForm)
        }
    }


    function toggleForm(e) {
      
        let commentContent =
          e.target.parentElement.parentElement.parentElement.children[0]
            .children[0];
        
        let form = e.target.parentElement.parentElement.parentElement.children[0].children[1]

        let editDeleteBtns = e.target.parentElement.parentElement.parentElement.children[1]
        
        if (e.currentTarget.param === "openCommentEdit") {

                form.style.display = "block"
                commentContent.style.display = "none"
                editDeleteBtns.style.display = "none"

            } else if  (e.currentTarget.param === "cancelCommentEdit" || form.style.display === "block") {
                form = e.target.parentElement.parentElement
                form.style.display = "none";

                

                commentContent = e.target.parentElement.parentElement.parentElement.children[0]
                commentContent.style.display = "flex"

                editDeleteBtns =
                  e.target.parentElement.parentElement.parentElement
                    .parentElement.children[1];

                editDeleteBtns.style.display = "block";

                }

        
    }
})
