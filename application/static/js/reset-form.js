$(document).ready(function() {
    let resetBtn = document.getElementById('reset-form')

    resetBtn.addEventListener('click', resetForm)
});

function resetForm() {

    // Clear all input fields
    
    let inputFields = document.querySelectorAll("input")


    for (input of inputFields) {

        if (input.value !== '') {

            if (input.classList.contains('select-dropdown')) {
                input.value = 'Choose a Genre:'
            } else {
                input.value = ""
            };

        };

    };

    // Return materializeCSS labels to unfocused state.


    let labels = document.querySelectorAll('label')

    for (x of labels) {
        
        if (x.classList.contains('active')) {
            x.classList.remove('active')
        }
    }
    
};