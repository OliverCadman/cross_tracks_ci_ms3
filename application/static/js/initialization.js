/* File contains all code required to initialize
MaterializeCSS features */
$(document).ready(function () {
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
  $(".datepicker").datepicker({
    yearRange: 75,
    format: 'yyyy-mm-dd'
  });
});
