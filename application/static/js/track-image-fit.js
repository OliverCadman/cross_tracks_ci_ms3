$(document).ready(function () {
  let x = window.matchMedia("(max-width: 992px)");

  if (x.matches) {
    let trackImageWrapperMed = document.getElementsByClassName("card-image");
    for (let i = 0; i < trackImageWrapperMed.length; i++) {
      trackImageWrapperMed[i].classList.remove("card-image");
      trackImageWrapperMed[i].classList.add("card-image-med");
    }
  }
});
