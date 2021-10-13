/* File contains all code required to initialize
MaterializeCSS features */
$(document).ready(function () {
  $(".dropdown-trigger").dropdown();
  $(".sidenav").sidenav({
    edge: "right",
    inDuration: 500,
    draggable: true,
  });
});
