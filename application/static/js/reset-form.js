$(document).ready(function() {
    let resetBtn = document.getElementById('reset-form')

    resetBtn.addEventListener('click', resetForm)
})

function resetForm() {
    console.log('click')
    let inputFields = document.querySelectorAll("input")
    console.log(inputFields)

    for (input of inputFields) {

        if (input.value !== '') {

            if (input.classList.contains('select-dropdown')) {
                input.value = 'Choose a Genre:'
            } else {
                input.value = "";
            }
            
        }
    }
    
}