$(document).on('click', '#eye', function(e) {
    console.log($(this).hasClass("fa-eye"))
    var x = document.getElementById("myinput");
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

function myfunc() {
    var message, x;
    message = document.getElementById("p1");
    message.innerHTML = "";
    x = document.getElementById("usr").value;
    try {
        if (x == "") throw "Empty";
        if (x != email) throw "Invalid";
    } catch (err) {
        message.innerHTML = "Invalid User" + err;
        console.log("Called");
    }
}