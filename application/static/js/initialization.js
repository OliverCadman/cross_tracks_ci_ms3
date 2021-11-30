/* File contains all code required to initialize
MaterializeCSS features */
$(document).ready(function () {
  console.log("ready")
  $(".modal").modal({
    opacity: 0.7,
  });
  $(".dropdown-trigger").dropdown();
  $(".sidenav").sidenav({
    edge: "left",
    inDuration: 500,
    draggable: true,
  });
  $(".tooltipped").tooltip();
  $("select").formSelect();
});
