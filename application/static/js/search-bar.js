$(document).ready(function () {
  $("#search-bar-icon").click(function () {
    document
      .getElementById("search-bar-wrapper")
      .classList.toggle("show-search-bar");
    console.log(document.getElementById("search-bar-wrapper").classList);

    let opaqueOverlay = document.getElementById("opaque-overlay");
    opaqueOverlay.classList.toggle("show-opaque-overlay");
  });

  let closeSearchBarIcon = document.getElementById("close-search-wrapper");
  closeSearchBarIcon.addEventListener("click", closeSearchBar);

  function closeSearchBar() {
    let searchBar = document.getElementById("search-bar-wrapper");
    let resultsWrapper = document.getElementsByClassName("results-wrapper")[0];
    let inputField = document.getElementById("search_input");
    let noResultsMsg = document.getElementById("no-result-msg");

    resultsWrapper.innerHTML = "";
    inputField.value = "";
    noResultsMsg.innerHTML = "";

    searchBar.classList.remove("show-search-bar");
  }
});

// Click outside search bar window to close search bar
// https://stackoverflow.com/questions/1403615/use-jquery-to-hide-a-div-when-the-user-clicks-outside-of-it?page=1&tab=votes#tab-top
$(document).mouseup(function (e) {
  let x = window.matchMedia("(min-width: 414px)");

  if (x.matches) {
    let searchWrapper = $("#search-bar-wrapper");

    if (searchWrapper.hasClass("show-search-bar")) {
      if (
        !searchWrapper.is(e.target) &&
        searchWrapper.has(e.target).length === 0
      ) {
        searchWrapper.removeClass("show-search-bar");

        $("#opaque-overlay").removeClass("show-opaque-overlay");
        $("#search_input").val("");
        $(".results-wrapper").html("");
      }
    }
  }
});
