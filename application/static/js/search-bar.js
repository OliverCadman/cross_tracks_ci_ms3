$(document).ready(function() {

    let searchBarButton = document.getElementById('search-bar-icon')
    
    searchBarButton.addEventListener("click", openSearchBar)



    function openSearchBar() {
        let searchBar = document.getElementById('search-bar-mobile-wrapper');

        searchBar.classList.toggle('show-search-bar');
    }
})