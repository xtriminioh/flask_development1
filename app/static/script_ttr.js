/*Config message - Begin (jquery)*/

$(document).ready(function () {
    $(".mybtn-login").click(function(){
        $(".message_wrapper").css("visibility","visible");
        $(".message_item").css("top","50%");
    });
    
    $(".close").click(function(){
        $(".message_wrapper").css("visibility","hidden");
        $(".message_item").css("top","-100%");
    });
});

/*Config message - End*/