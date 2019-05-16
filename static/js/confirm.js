/*toggle eye icon for confirm password*/

$(document).on('click', '#eyes', function(e) {
    var x = document.getElementById("confirm_password");
    if (x.type === "password") {
        x.type = "text";
        $(this).removeClass("fa-eye")
        $(this).addClass("fa-eye-slash")
        document.getElementsByTagName("span").className = "fa fa-fw fa-eye";

    } else {
        x.type = "password";
        $(this).removeClass("fa-eye-slash")
        $(this).addClass("fa-eye")
    }

})

/*toggle eye icon for new password*/
$(document).on('click', '#eye', function(e) {
    var x = document.getElementById("new_password");
    if (x.type === "password") {
        x.type = "text";
        $(this).removeClass("fa-eye")
        $(this).addClass("fa-eye-slash")
        document.getElementsByTagName("span").className = "fa fa-fw fa-eye";

    } else {
        x.type = "password";
        $(this).removeClass("fa-eye-slash")
        $(this).addClass("fa-eye")
    }

})