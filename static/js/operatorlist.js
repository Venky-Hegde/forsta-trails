//Email Validation



// show data table
$("#mydata").dataTable();

//password show hide

$(document).on('click', '#passwordshow', function(e) {
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

//     var input = document.querySelector("#phone");
//  window.intlTelInput(input, {
//    utilsScript: "../static/build/js/utils.js",
//  });
//
//     var input = document.querySelector("#editphone");
//  window.intlTelInput(input, {
//    utilsScript: "../static/build/js/utils.js",
//  });

//onclick edit operator

$(document).on('click', '#edit_operator', function(e) {
    $("#edit_operatordata").modal('show');
    $('#email').val($(this).parents('tr').find('input[name="email"]').val())
    $('#editphone').val($(this).parents('tr').find('input[name="phone_number"]').val())
    $('#first_name').val($(this).parents('tr').find('input[name="first_name"]').val())
    $('#last_name').val($(this).parents('tr').find('input[name="last_name"]').val())
    $('#company_name').val($(this).parents('tr').find('input[name="company_name"]').val())
    $('#User_id').val($(this).parents('tr').find('input[name="id"]').val())
    $('#vale').val($(this).parents('tr').find('input[name="password"]').val())
    $('#Company_id').val($(this).parents('tr').find('input[name="company_id"]').val())
    var interview_services = $(this).parents('tr').find('input[name="interview_services"]').val()
        if (interview_services == "True"){
                        $('#Interviewer').prop('checked', true);

        }
        else{
                                $('#Interviewer').prop('checked', false);


        }
})
//
//$('.checkbox_class').on('change', function(){ // on change of state
//    if(this.checked) {
//        $("#interviservice_msg").removeClass("hide")
//  setTimeout(function(){ $('#interviservice_msg').addClass('hide') }, 3000);
//$("#interviservice_msg2").removeClass("hide")
//  setTimeout(function(){ $('#interviservice_msg2').addClass('hide') }, 3000);
//
//   }
//   else{
//           $("#interviservice_msg").addClass("hide")
//           $("#interviservice_msg2").addClass("hide")
//
//   }
//
//});


//tagify

