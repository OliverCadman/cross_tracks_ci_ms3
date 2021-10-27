document.addEventListener("DOMContentLoaded", function() {
    collectLikeButtons();
})

function collectLikeButtons() {
    removeLikeButtons = document.getElementsByClassName("remove-like")
    
    for (let i = 0; i < removeLikeButtons.length; i++) {
        removeLikeButtons[i].addEventListener("click", removeLike)
    }

}

function removeLike(e) {
    e.preventDefault();
    $.ajax(this.href, {
        success: function(res) {
            console.log(res)
            let removedTrack = e.target.parentElement.parentElement.parentElement.parentElement
            removedTrack.remove();
        }
    })
}