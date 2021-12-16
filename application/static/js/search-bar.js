$(document).ready(function () {
  $("#search-bar-icon").click(function () {
    document
      .getElementById("search-bar-wrapper")
      .classList.toggle("show-search-bar");

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
    let opaqueOverlay = document.getElementById("opaque-overlay");

    resultsWrapper.innerHTML = "";
    inputField.value = "";

    if (noResultsMsg) {
       noResultsMsg.innerHTML = "";
    }
   
    if (searchBar.classList.contains("show-search-bar")) {
      searchBar.classList.remove("show-search-bar");
      opaqueOverlay.classList.remove("show-opaque-overlay")
    }   
  }
});
