$(document).ready(function($) {
    $(".clickable-row").on('click', function(e) {
        if(e.ctrlKey){
            window.open($(this).data("url"), "_blank");
        }
        else{
            window.open($(this).data("url"), "_self");
        }
    });
});
