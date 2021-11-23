$(document).ready(function(){
    displayToast();
})

function displayToast(flashMessages){
    for (let alert in flashMessages){

        alertHTML = `${flashMessages[alert]}`

        M.toast({
            html: alertHTML,
            classes: 'flash-message center-align',
            displayLength: 3000
        });
    }
}
