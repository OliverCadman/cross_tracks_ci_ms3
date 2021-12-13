$(document).ready(function () {
  const fileInput = document.getElementById("profile_image");

  fileInput.addEventListener("input", checkFilesize);
  fileInput.sizeParam = this;

  function checkFilesize(e) {
    document.cookie = `filesize=${e.currentTarget.files[0].size}`;
  }
});
