$(document).ready(function () {
  document.getElementById("profile_image").onchange = function (e) {
    e.preventDefault();

    document.cookie = `filesize=${e.currentTarget.files[0].size}`;

    console.log(document.cookie.split("=")[1]);

    let allowedFilesize = 0.5 * 1024 * 1024;

    if (document.cookie.split("=")[1] > allowedFilesize) {
      imgTooLargeToast("Images must be less than 500KB");
    } else {
      document.getElementById("edit-profile-img-form").submit();
    }
  };
});
