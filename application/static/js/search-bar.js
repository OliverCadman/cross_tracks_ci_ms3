$(document).ready(function() {

    let searchBarButtons = document.getElementsByClassName('search-bar-icon')

    for(let i = 0; i < searchBarButtons.length; i++){
        
         searchBarButtons[i].addEventListener("click", openSearchBar);
        }

    let closeSearchBarIcon = document.getElementById("close-search-wrapper");
    closeSearchBarIcon.addEventListener("click", closeSearchBar) 
    


    function openSearchBar() {
        let searchBar = document.getElementById('search-bar-wrapper');
        console.log('click')
        searchBar.classList.toggle('show-search-bar');
    }

    
    function closeSearchBar(){
        let searchBar = document.getElementById('search-bar-wrapper')
        let resultsWrapper = document.getElementsByClassName("results-wrapper")[0]
        let inputField = document.getElementById('search_input')

        resultsWrapper.innerHTML = ""
        inputField.value = ""

        searchBar.classList.remove('show-search-bar')
    }
})