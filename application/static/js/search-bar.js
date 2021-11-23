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

        let opaqueOverlay = document.getElementById("opaque-overlay")
        opaqueOverlay.classList.toggle('show-opaque-overlay')
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

// Click outside search bar window to close search bar 
// https://stackoverflow.com/questions/1403615/use-jquery-to-hide-a-div-when-the-user-clicks-outside-of-it?page=1&tab=votes#tab-top
$(document).mouseup(function(e) {
     let searchWrapper = $("#search-bar-wrapper");

     if(searchWrapper.hasClass('show-search-bar')) {

         if (
           !searchWrapper.is(e.target) &&
           searchWrapper.has(e.target).length === 0
         ) {
           searchWrapper.removeClass('show-search-bar');

           $('#opaque-overlay').removeClass('show-opaque-overlay');
           $('#search_input').val('');
           $('.results-wrapper').html('');
            
     }

     }
})