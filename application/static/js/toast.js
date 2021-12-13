$(document).ready(function(){
    displayToast();
})

function displayToast(flashMessages){
    for (let alert in flashMessages){

        let alertHTML = `${flashMessages[alert]}`

        M.toast({
            html: alertHTML,
            classes: 'flash-message center-align',
            displayLength: 3000
        });
    }
}

function imgTooLargeToast(message) {
    let alertHTML  = `${message}`

    M.toast({
        html: alertHTML,
        classes: 'flash-message center-align',
        displayLength: 3000
    })
}
