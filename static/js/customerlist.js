//email validation
$("input[name='email']").change(function() {

    $.ajax({
        url: "/ckeckmail/",
        method: 'post',
        data: {
            "email": $(this).val()
        },
        dataType: 'json',
        success: function(data) {
            if (!data.status) {

                $('#unique_email').removeClass('hide');
                $('#uni_email').removeClass('hide');

                $('#unique_email').addClass('show');
                $('#uni_email').addClass('show');
                $('#e_mail').val('')
                $('#e_id').val('')


            } else {
                $('#unique_email').removeClass('show');
                $('#uni_email').removeClass('show');

                $('#unique_email').addClass('hide');
                $('#uni_email').addClass('hide');

            }
                            $('#prim_skills').val('')



        }
    });

})




// DATA TABLE
//$('#dashboard_data').dataTable();
$('#customer_data,#mydata,#interview_table',).dataTable();

 $('#profile_data').dataTable({
        responsive: true,
        "order": [[ 9, "desc" ]]
    });





// SHOW HIDE PASSWORD
function passwordshow() {
    var x = document.getElementById("mypassword");
    if (x.type === "password") {
        x.type = "text";
        document.getElementsByTagName("span").className = "fa fa-fw fa-eye";

    } else {
        x.type = "password";
    }

}

function show() {
    var x = document.getElementById("password");
    if (x.type === "password") {
        x.type = "text";
        document.getElementsByTagName("span").className = "fa fa-fw fa-eye";

    } else {
        x.type = "password";
    }

}


//  intl input
//$('#profile_data').dataTable();
//     var input = document.querySelector("#cust_phone");
//  window.intlTelInput(input, {
//    utilsScript: "../static/build/js/utils.js",
//  });
//     var input = document.querySelector("#editphone");
//  window.intlTelInput(input, {
//    utilsScript: "../static/build/js/utils.js",
//  });
//       var input = document.querySelector("#phone_number");
//  window.intlTelInput(input, {
//    utilsScript: "../static/build/js/utils.js",
//  });


//edit customer
$(document).on('click', '#editcustomer', function(e) {
    $('#email').val($(this).parents('tr').find('input[name="email"]').val())
    $('#phone_number').val($(this).parents('tr').find('input[name="phone_number"]').val())
    $('#firstname').val($(this).parents('tr').find('input[name="first_name"]').val())
    $('#last_name').val($(this).parents('tr').find('input[name="last_name"]').val())
    $('#company_name').val($(this).parents('tr').find('input[name="company_name"]').val())
    $('#User_id').val($(this).parents('tr').find('input[name="id"]').val())
    $("#editcustomerdata").modal('show');

})

//edit my user.
$(document).on('click', '.edit_myuser', function(e) {
    $('#email_user').val($(this).parents('tr').find('input[name="email"]').val())
    $('#phone_number_user').val($(this).parents('tr').find('input[name="phone_number"]').val())
    $('#firstname_user').val($(this).parents('tr').find('input[name="first_name"]').val())
    $('#last_name').val($(this).parents('tr').find('input[name="last_name"]').val())
    $('#company_name_user').val($(this).parents('tr').find('input[name="company_name"]').val())
    $('#User_id_user').val($(this).parents('tr').find('input[name="id"]').val())

})



// open diag
function openfileDialog() {
    $("#fileLoader").click();


}


next_profiles = []
next_profiles_id = []
rowIndex = "";

//open edit profile
function editprofile() {
    alert($(this).parents('tr').html())
}
profile_data_change = false
//open edit profile
$(document).on('click', '.changeprofile', function(e) {
profile_data_change = false

getallcompanylist()
document.getElementById("validate_profiles").disabled = true;
document.getElementById("validate_profiles1").disabled = true;

document.getElementById("attach_profiles_resume").disabled = false;

    row_index = $(this).closest("tr").index();
    document.getElementById("row_index_repository").value = row_index;

function checkChange($this){
var value = $this.val();

   var sv=$this.data("stored");

   if(value!=sv)
       $this.trigger("simpleChange");

}

$(this).data("stored",$(this).val());
   $("input").bind("keyup",function(e){
   checkChange($(this));
});


$("input").bind("simpleChange",function(e){
profile_data_change = true
document.getElementById("validate_profiles").disabled = false;
document.getElementById("validate_profiles1").disabled = false;

});


$('.checkbox_class').on('change', function(){ // on change of state
    if(this.checked) {
profile_data_change = true
document.getElementById("validate_profiles").disabled = false;
document.getElementById("validate_profiles1").disabled = false;

   }
});


while(next_profiles.length > 0) {
    next_profiles.pop();
}
while(next_profiles_id.length > 0) {
    next_profiles_id.pop();
}
var table = document.getElementById("data_table_repository");

for (var i = 1, row; row = table.rows[i]; i++) {
var list_profiles = $(row).find('.changeprofile').attr('id')
var list_profiles_id = $(row).find('.changeprofile').attr('value')

next_profiles.push(list_profiles)
next_profiles_id.push(list_profiles_id)
}
console.log(next_profiles)
console.log(next_profiles_id)

console.log($(this).parents('tr').next().find('.changeprofile').attr('id'))
//var rows = document.getElementsByTagName('tr');
//for(var x = 0, xLength = rows.length; x < xLength; x++) {
//   console.log('rowIndex=' + rows[x].rowIndex);
//   console.log(rows[x])
//   console.log($( rows[x]).find('.editbtn_d').attr('id'))
//}
//$(this).parents('tr').find('td:eq(0)').html()
//console.log($(this).parents('tr').next().html())
//($(this).parents('tr').html())


   var p_id = $(this).attr('value')
   $('input[id="pro_id"]').val($(this).attr('value'))

   show_profile_details(p_id)





//    $('#email_address').val($(this).parents('tr').find('input[name="email_address_hide"]').val())



    var file_name = $(this).attr('id')


    var extention = file_name.slice((file_name.lastIndexOf(".") - 1 >>> 0) + 2)

    if (extention == "pdf") {

        var file_type = '../media/'+file_name
        $('#resume_pdf').attr('data',file_type)

        $('#resume_doc').addClass('hide')
        $('#resume_pdf').removeClass('hide')

    } else if (extention == "doc" || extention == "docx") {


        var new_file = "https://docs.google.com/gview?url=" + location.protocol + "//" + window.location.host + "/media/" + file_name + "&embedded=true"
        $('#resume_pdf').addClass('hide')
        $('#resume_doc').removeClass('hide')
        $('#resume_doc').attr('src', new_file)


    }

    else if (extention == "odt") {
         var new_file = "https://docs.google.com/gview?url=" + location.protocol + "//" + window.location.host + "/media/" + file_name + "&embedded=true"
        $('#resume_pdf').addClass('hide')
        $('#resume_doc').removeClass('hide')
        $('#resume_doc').attr('src', new_file)

    }


    $("#editprofile").modal('show');
})

function show_profile_details(p_id){

   data={"p_id" : p_id}
        $.ajax({
         data     : data,
         datatype : 'JSON',
         url      : "/show_profile_details/",
         method   : "get",
         success   : function(data){
       console.log(data, "ggggggggggggggggggggg")
               $.each(data.details, function(key, value){


               $('input[id="email_address"]').val(value['candidate_email'])
               $('input[id="experience"]').val(value['experience'])
               $('input[id="editphone"]').val(value['phone_number'])
               $('input[id="first_name"]').val(value['candidate_name'])
               $('input[id="primary_skills"]').val(value['primary_skills'])
               $('input[id="current_company"]').val(value['current_company'])
               $('input[id="current_ctc"]').val(value['current_ctc'])
               $('input[id="expected_ctc"]').val(value['expected_ctc'])
               $('input[id="notice_period"]').val(value['notice_period'])
               $('input[id="current_location"]').val(value['location'])
               $('input[id="current_role"]').val(value['current_role'])
               $("textarea#resume_id_notes").val(value['notes']);
$(".tags_container").empty()


               if(value['is_interviewer'] == true){
              $("#Interviewer").prop('checked' , true);


              }

              else{

              $("#Interviewer").prop('checked' , false);

              }







//                    $('input[id="alternate_phone_number"]').val(value['alternate_phone_number'])
//$('.tag_input').tagsinput('add',  { id: 1, text: 'some tag' });
if( value['interview_skills'] != "null"){


var str = value['interview_skills']
    var array = str.split(",");
   for(var i=0 ; i < array.length; i++){

 container = "<span class='tag'>"+ array[i] + " <span class='close'></span></span> "
 $(".tags_container").append(container)   }


 }
//                    $('#interview_skills').tagsinput('add', { "value": 1 , "text": "Amsterdam"  });

//                    alert(value['interview_skills'])
//                        $('#interview_skills').tagsinput('add', "java");

//               $('input[id="interview_skills"]').val(value['interview_skills'])

//    document.getElementById("last_updated").innerHTML = "Last updated:" + value["updated_on"];

               if(value['availability']=='yes'){

                $('#availability').prop('checked', true); // Checks it

              }
               else{
                 $('#availability').prop('checked', false); // Checks it

              }




})

}

});


}

$(document).on('click', '.editbtn_d ', function(e) {
    $("#viewResume").modal('show')
    var file_name = $(this).attr('id')

   var p_id = $(this).attr('value')
   $('input[id="pro_id_jpa"]').val($(this).attr('value'))


    var extention = file_name.slice((file_name.lastIndexOf(".") - 1 >>> 0) + 2)

    if (extention == "pdf" ||extention == "pdf " || extention == " pdf"  ) {
        var file_type = '../media/'+file_name
        $('#viewResume_pdf').attr('data', file_type)

        $('#viewResume_doc').addClass('hide')
        $('#viewResume_pdf').removeClass('hide')

         }else if(extention == "doc" ||extention == "docx" ){


        var new_file = "https://docs.google.com/gview?url=" + location.protocol + "//" + window.location.host + "/media/" + file_name + "&embedded=true"
        $('#viewResume_pdf').addClass('hide')
        $('#viewResume_doc').removeClass('hide')
        $('#viewResume_doc').attr('src', new_file)


    }

open_notes_model(p_id)

})

$(document).on('click', '.profile_cancel ', function(e) {
if(profile_data_change == true){
msg= 'Do you want to save the changes?'

$.confirm({
    title  : '',
    content:msg ,
    buttons: {
    cancel: function () {
    $("#editprofile").modal('hide');

        },


        save: function () {
        update_profile()
    $("#editprofile").modal('hide');

}



}
});



}
else {
    $("#editprofile").modal('hide');

}

});




$(document).on('click', '.resume_openn ', function(e) {
    $("#resume_open").modal('show')

    var file_name = $(this).attr('id')
    var extention = file_name.slice((file_name.lastIndexOf(".") - 1 >>> 0) + 2)

    if (extention == "pdf") {
        var file_type = '../media/' + file_name
        $('#resume_pdff').attr('data', file_type)
        $('#resume_docc').addClass('hide')
        $('#resume_pdff').removeClass('hide')

    } else if (extention == "doc" || extention == "docx") {


        var new_file = "https://docs.google.com/gview?url=" + location.protocol + "//" + window.location.host + "/media/" + file_name + "&embedded=true"
        $('#resume_pdff').addClass('hide')
        $('#resume_docc').removeClass('hide')
        $('#resume_docc').attr('src', new_file)


    }



})

$(document).on('click', '.editbtn_dd ', function(e) {
    $("#viewSearchedResume").modal('show')


    var file_name = $(this).parents('tr').find('.resume_open').attr('id')

    var extention = file_name.slice((file_name.lastIndexOf(".") - 1 >>> 0) + 2)

    if (extention == "pdf") {
        var file_type = '../media/' + file_name
        $('#viewSearchedResume_pdf').attr('data', file_type)

        $('#viewSearchedResume_doc').addClass('hide')
        $('#viewSearchedResume_pdf').removeClass('hide')

    } else if (extention == "doc" || extention == "docx") {


        var new_file = "https://docs.google.com/gview?url=" + location.protocol + "//" + window.location.host + "/media/" + file_name + "&embedded=true"
        $('#viewSearchedResume_pdf').addClass('hide')
        $('#viewSearchedResume_doc').removeClass('hide')
        $('#viewSearchedResume_doc').attr('src', new_file)


    }



})
//
//function moveScroll(){
//    var scroll = $(window).scrollTop();
//    var anchor_top = $("#dashboard_data").offset().top;
//    var anchor_bottom = $("#bottom_anchor").offset().top;
//    if (scroll>anchor_top && scroll<anchor_bottom) {
//    clone_table = $("#clone");
//    if(clone_table.length == 0){
//        clone_table = $("#dashboard_data").clone();
//        clone_table.attr('id', 'clone');
//        clone_table.css({position:'fixed',
//                 'pointer-events': 'none',
//                 top:0});
//        clone_table.width($("#dashboard_data").width());
//        $("#dashboard_details").append(clone_table);
//        $("#clone").css({visibility:'hidden'});
//        $("#clone thead").css({visibility:'visible'});
//    }
//    } else {
//    $("#clone").remove();
//    }
//}
//$(window).scroll(moveScroll);


// reset password
$(document).on('click', '#change', function(e) {
    $("#change_password").modal('show')
})


$(document).on('click', '#file', function(e) {

    var file_type = $(this).parents('tr').find('input[name="resume_name"]').val()


    var file_name = file_type.split('/')[2]




    var extention = file_type.slice((file_type.lastIndexOf(".") - 1 >>> 0) + 2)


    if (extention == "pdf") {


        $('#resume_pdff').attr('data', file_type)

        $('#resume_docc').addClass('hide')
        $('#resume_pdff').removeClass('hide')

    } else if (extention == "doc" || extention == "docx") {
        var new_file = "https://docs.google.com/gview?url=" + location.protocol + "//" + window.location.host + "/media/" + file_name + "&embedded=true"

        $('#resume_pdff').addClass('hide')
        $('#resume_docc').removeClass('hide')
        $('#resume_docc').attr('src', new_file)


    }
    $("#resume_open").modal('show')
})


//sidenav open close
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
}

// tooltip toggle
$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();
    $.fn.dataTableExt.sErrMode = 'throw';

});




//To disable Attach
$('#sub').prop("disabled", true);
$('input:checkbox').click(function() {
    if ($(this).is(':checked')) {
        $('#sub').prop("disabled", false);
    } else {
        if ($('.chk').filter(':checked').length < 1) {
            $('#sub').attr('disabled', true);
        }
    }
});


//List jobs




function Openmodel(com_id) {
console.log(com_id)
  document.getElementById("companyid_job").value = com_id;

//$('input[name="companyname"]').value = com_name;


    if (com_id == '') {
        swal("please try again")

    } else {
        $('#create_job').modal('show')
    }
}
var company_id = ''
var job_id = ''
var resume_id = ''
var profiles_id = []

function JoblistCall(id) {
 $("#dash_board_job option").remove();
                   $("#dash_board_job").append('<option value="0" selected>select all</option>');

$("#edit_resume_job option").remove();
                   $("#edit_resume_job").append('<option id="0" value="0" selected>select all</option>');


console.log(id,"this is job id............................")

    $('#companyid').val(id)
    $.ajax({
        datatype: 'JSON',
        data : {"com_id" : id},
        url: "/company/joblist/",
        method: "get",
        success: function(data) {
        console.log(joblist_data)
        if(data.jobs.length > 0 ){

            $('#joblist_data').empty()
            $.each(data.jobs, function(key, value) {
                        console.log(data , "aaaaaaaaaaaaaaaaaaaaaaaaaa")




                    $("#dash_board_job").append('<option value=" ' + value['id'] + ' ">' + value["job_title"] + '</option>')

                        $("#edit_resume_job").append('<option value=" ' + value['id'] + ' ">' + value["job_title"] + '</option>')


            })



        }
        else{
                      $('#joblist_data').empty()
                    data={"job_id" : 0}
            }

        }
    });

}



//open conversation modal and chat functionalities
var job_id = ''
$(document).on('click', '.get_chat', function(event) {


    resume_id = $(this).attr('id')
        job_id = $("#joblist_data .main_card.active").attr('id')
console.log(job_id , "which is job id for conversation................")
    getallmessages(resume_id, job_id)

})




function getallmessages(job_id,jpa_id ,company_id) {
    $('#messageModal').modal('show');

    $.ajax({

        data: '',
        datatype: 'JSON',
        url: "/conversationdisplay/?jpaid=" + jpa_id + "&job_id=" + job_id,
        method: "get",
        success: function(data) {
            $('.msg_card_body').empty()

            $.each(data, function(key, value) {

                if (value.send_by == true) {

                    $('.msg_card_body').append('<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + value.msg + '<span class="msg_time_send">' + value.sn + ' </span></div><div class="img_cont_msg"><i class="fa fa-user-o" aria-hidden="true"></i></div></div>')

                } else {

                    $('.msg_card_body').append('<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><i class="fa fa-user-o" aria-hidden="true" ></i></div><div class="msg_cotainer">' + value.msg + '<span class="msg_time">8:40 AM, Today</span></div></div>')


                }

            })

            console.log(data)
        }
    })
document.getElementById("jpa_id").value = jpa_id;
document.getElementById("job_id").value = job_id;
document.getElementById("company_id").value = company_id;

}




$(document).on('click', '.send_btn', function(event) {
   jpa_id = document.getElementById("jpa_id").value;
 job_id = document.getElementById("job_id").value;
 company_id = document.getElementById("company_id").value;

    var message = $('#text_msg_value').val()
    postmessages(jpa_id, job_id,company_id, message)



})




function postmessages(jpa_id, j_id,company_id, chat) {

    data = {
        "jobid": j_id,
        "jpa_id": jpa_id,
        "chat": chat,
        "company_id" : company_id,
    };

    console.log(data, "aaaaaaaaaaaaaaaaaaaaA")
    $.ajax({

        data: data,
        datatype: 'JSON',
        url: "/conversation/",
        method: "post",
        success: function(data) {

            console.log(data,"after saving")
            $('.msg_card_body').append('<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + chat + '<span class="msg_time_send">9:10 AM, </span></div><div class="img_cont_msg"><i class="fa fa-user-o" aria-hidden="true"></i></div></div>')
            $('#text_msg_value').val('')
            $(".cardsd").animate({
                scrollTop: $(document).height()
            }, 1000);

        }
    })

}


/* button hide and show if selected company is all*/
$(function() {
    $('#ma').change(function() {
        var opt = $(this).val();
        if (opt == '0') {
            $('#btn').hide();
            $('#btn1').hide();
        } else {
            $('#btn').show();
            $('#btn1').show();
        }
    });
});


//hide and show button if no jobs
$(document).ready(function() {
    if ($('#joblist_data').is(':empty')) {
        $('#btn1').hide();
    } else {
        $('#btn1').show();

    }
});


//delete customer
function delete_cust(o_id, c_id) {


$.confirm({
    title: 'Delete Customer',
    content: 'Are you sure you want to delete? It will be permanently deleted',
    buttons: {
    cancel: function () {

        },


        delete: function () {



            document.location.href = "/deleteoper/?op_id=" + o_id + "&comid=" + c_id;

        },
        }
    });

}






//delete profile
$(document).on('click', '.delete_profile', function(event) {


    resume_id = $(this).attr('id')

job_id = $("#joblist_data .main_card.active").attr('id')

     console.log(job_id, "this is job id to delete...............")
    delete_jobprofile(resume_id,job_id)

})

//delete atached profile
function delete_jobprofile(jpa_id, job_id) {
company_id = $("#dash_board_table option:selected").val();
job_id      = $("#dash_board_job  option:selected").val();



data = {"jpa_id" : jpa_id , "job_id" : job_id }


$.confirm({
    title: 'Delete Profile',
    content: 'Are you sure you want to delete?',
    buttons: {
    cancel: function () {

        },


        delete: function () {


            $.ajax({

                data : data,
                datatype: 'JSON',
                url: "/deletejobprofile/",
                method: "get",

                success: function(data) {
//                    data={"job_id" : data.job_id}
//                    ajaxDataTableCall(data)

                  toastr.success(data.msg)
                  dashboardLoad(company_id, job_id)
          }

          });
}



}
});

      }

$(document).on('click', '.delete_job', function(event) {

    job_id = ($(this).parents('.main_card').attr('id'))


    delete_job(job_id)

})

function delete_job(j_id){
$.ajax({


                datatype: 'JSON',
                url: "/checkingjob/?job_id="+ j_id,
                method: "get",

                success: function(data) {
                if (data.msg == "This job cannot be deleted as it contains profiles") {
                  toastr.success(data.msg)

                                                    }
else{


                    $.confirm({
    title: 'Delete  Job',
    content: 'Are you sure you want to delete?',
    buttons: {
    cancel: function () {

        },


        delete: function () {

         $.ajax({
        url: "/deletejobs/?job_id=" + j_id,
        method: 'get',
        dataType: 'json',
        success: function(data) {

            toastr.success(data.msg);
            dashboardLoad(c_id,0)


          }

          });



















                }
}

});
    }
}
          });
}

//delete profile
function delete_profile(p_id) {





$.confirm({
    title: 'Delete  Profile',
    content: 'Are you sure you want to delete?',
    buttons: {
    cancel: function () {

        },


        delete: function () {



    $.ajax({
        url: "/deleteunattchedprofile/?p_id=" + p_id,
        method: 'get',
        dataType: 'json',
        success: function(data) {

            toastr.success(data.msg);
            profileRepositoryload()

          }

          });
}



}
});

      }
//press enter to send message

var input = document.getElementById("text_msg_value");
input.addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        document.getElementById("send_button").click();
    }
});


//excel export
function customert_list_to_excel() {
    document.location.href = "{% url 'customerlisttoexcel'%}";
}


function profile_list_to_excel() {
    document.location.href = "{% url 'profilelisttoexcel'%}";
}



 function jpa_list_to_excel(j_id){

         $.ajax({
     url :"/jpalisttoexcel/?jobid="+j_id,
     method : 'get',
     success:function(data){
    if (data.fname == undefined){
    swal("please attach profile")
    }
    else{
     linkHref="../media/"+data.fname
     window.open(linkHref, '_blank');
  }}

});



         }



//add operator
function add_operator() {

    var first_name = document.getElementById("fi_name").value;
    var last_name = document.getElementById("la_name").value;
    var email = document.getElementById("e_id").value;
    var company_name = document.getElementById("c_name").value;
    var password = document.getElementById("myinput").value;
    var phone_number = document.getElementById("operphone").value;
    var data = {
        first_name: first_name,
        last_name: last_name,
        email: email,
        company_name: company_name,
        password: password,
        phone_number: phone_number,
    }


    $.ajax({

        url: "/addoperator/",
        method: 'post',
        data: data,
        dataType: 'json',
        success: function(data) {

            swal(data.msg);
            window.location.reload();

        }


    });

}



// add operator form validation
function validate() {

    $("#form").validate({
        rules: {

            "email": {
                required: true,
            },

            "first_name": {
                required: true,
            },
            "company_name": {
                required: true,
            },
            "password": {
                required: true,
            },
            "phone_number": {
                required: true,
                minlength: 8,
                maxlength: 12


            }
        },
        messages: {
            "name": {
                required: "Please, enter a name"
            },
            "email": {
                required: "This field is required.",
                email: "Email is invalid"
            }
        },

        submitHandler: function(form) { // for demo
            add_operator()
        }


    });

}


// reload same page with refresh
$('span[data-toggle="tab"]').on('show.bs.tab', function(e) {
    localStorage.setItem('activeTab', $(e.target).attr('href'));
});

$(document).ready(function() {
    var activeTab = localStorage.getItem('activeTab');
    console.log(activeTab);

    if (activeTab) {
        $('span[href="' + activeTab + '"]').tab('show').toggleClass('active');


    } else {

        $($('span[data-toggle="tab"]')[0]).tab('show').toggleClass('active');
        dashboardLoad(0,0)

    }

})

//stay on same selected company
$(function() {
    if (localStorage.getItem('ma')) {
        $("#ma option").eq(localStorage.getItem('ma')).prop('selected', true);
    }

   $("#ma").on('change', function() {
        localStorage.setItem('ma', $('option:selected', this).index());
    });
});




//speech recognizer
//      var company_name="{{request.user.company.company_name}}"
//         var  =document.getElementById('search');
//
//         function startConverting(){
//
//         if('webkitSpeechRecognition' in window){
//         console.log("aaaaaaaaa")
//         var speechRecognizer = new webkitSpeechRecognition();
//         speechRecognizer.continous = true;
//         speechRecognizer.interimResults = true;
//         speechRecognizer.lang = 'en-IN';
//         speechRecognizer.start();
//         console.log("aaaaaaaaaaa")
//
//
//         var finalTranscripts = '';
//
//         speechRecognizer.onresult = function(event){
//            var interimTranscripts = '';
//            for(var i = event.resultIndex; i < event.results.length; i++){
//                var transcript = event.results[i][0].transcript;
//                transcript.replace("\n", "</br>");
//                if(event.results[i].isFinal){
//                     finalTranscripts += transcript;
//
//                }else{
//                     interimTranscripts += transcript;
//
//                }
//
//            }
//
//            r.innerHTML = finalTranscripts  + '<span style="color:#999">' + interimTranscripts + '</span>';
//             console.log(r.innerHTML,"cccccccccccccccccc");
//             $("#id_smart_search").trigger('click');
//         $('#search').val(interimTranscripts)
//
//
//         };
//         speechRecognizer.onerror = function(event){
//
//
//
//         };
//
//
//         }else{
//         r.innerHTML = "error msg pls upgrade";
//         }
//
//
//         }


//reset button functionality
function getallprofiles() {
    window.location.reload();
}

// check duplicate email
//       $( document ).ready(function() {
//         {%if success == "False" %}
//            $('#checkemail').modal('show')
//         {% endif%}
//         });


//select_roles
function select_roles() {
    if ("operator" == $('#aioConceptName').find(":selected").val()) {
        $('#com_name').val(company_name)

    } else {
        $('#com_name').val("")

    }
}


//check duplicate email

$("input[name='e_mail']").change(function() {
    $.ajax({
        url: "/ckeckmail/",
        method: 'post',
        data: {
            "e_mail": $(this).val()
        },
        dataType: 'json',
        success: function(data) {
            if (!data.status) {
                $('#unique_email').removeClass('hide');
                $('#unique_email').addClass('show');
                $('#e_mail').val('');
            } else {
                $('#unique_email').removeClass('show');

                $('#unique_email').addClass('hide');

            }

        }
    });

})

//check duplicate company name


$("input[name='company_name']").change(function() {
    $.ajax({
        url: "/checkcompany/",
        method: 'post',
        data: {
            "company_name": $(this).val()
        },
        dataType: 'json',
        success: function(data) {
            if (!data.status) {
                $('#uniqu_companyname').removeClass('hide');
                $('#uniqu_companyname').addClass('show');
                $('#com_name').val('')
            } else {
                $('#uniqu_companyname').removeClass('show');

                $('#uniqu_companyname').addClass('hide');

            }

        }
    });

})


//get unattached profiles
function getUnattchedProfiles(jobid, compid) {
document.getElementById("attach_job_id").value = jobid;
document.getElementById("attach_com_id").value = compid


    $.ajax({

        data: jobid,
        datatype: 'JSON',
        url: "/attachprofiles/?jobid=" + jobid + "&comid=" + compid,
        method: "get",
        success: function(data) {
            console.log("data is ", data)

            $('#show_attached_profiles').removeClass('show')

            $('#show_attached_profiles').addClass('hide')
             $('#dashboard_details').removeClass('show')
                        $('#dashboard_details').addClass('hide')

                        $('#company_dropdown').addClass('hide')
                        $('#job_dropdown').addClass('hide')
                         $('#company_attach').removeClass('hide')
                        $('#company_attach').addClass('show')

            $('#new_profiles').removeClass('hide')
            $('#new_profiles').addClass('show')

            $('#new_profile_table_row').empty()
$('#unAttachedProfiles').DataTable().clear().destroy();
$('#table_id').empty();


            if (data.data.length > 0) {
                $.each(data.data, function(key, value) {
                    var extension = value['resume_name'].slice(( value['resume_name'].lastIndexOf(".") - 1 >>> 0) + 2)
                    console.log(value["availability"])
                    if(value["availability"]=="yes")
                    {

                    $('#new_profile_table_row').append("<tr ><td><input class='styled-checkbox second_layer'  id=" + value['id'] + " type='checkbox'  value=" + value['id'] + "  name='issue_category'><label for=" + value['id'] + " class='univ-43'></label></td> <td scope='col'>" + value['candidate_name'] + "</td>'<td value='true'><input type='hidden' value='true'><i class='dot'></i></td><td scope='col'>" + value['candidate_email'] + "</td><td scope='col'>" + value['phone_number'] + "</td><td scope='col'>" + value['current_role'] + "</td><td scope='col'>" + value['primary_skills'] + "</td><td scope='col'>" + value['current_company'] + "</td><td scope='col'>" + value['experience'] + "</td><td scope='col'>" + value['current_ctc'] + "</td><td scope='col'>" + value['expected_ctc'] + "</td><td scope='col'>" + value['notice_period'] + "</td><td scope='col'>" + value['updated_on'] + "</td><td scope='col' class='resume_open' ><img src='../static/css/document-edit-icon.png' width='22px' class='changeprofile' id='"+ value['resume_name'] +"' value='"+value['id']+"' '></img></td></tr>")
                    }
                    else{
                     $('#new_profile_table_row').append("<tr ><td><input class='styled-checkbox second_layer'  id=" + value['id'] + " type='checkbox'  value=" + value['id'] + "  name='issue_category'><label for=" + value['id'] + " class='univ-43'></label></td> <td scope='col'>" + value['candidate_name'] + "</td>'<td ><input type='hidden' value='false'><i ></i></td><td scope='col'>" + value['candidate_email'] + "</td><td scope='col'>" + value['phone_number'] + "</td><td scope='col'>" + value['current_role'] + "</td><td scope='col'>" + value['primary_skills'] + "</td><td scope='col'>" + value['current_company'] + "</td><td scope='col'>" + value['experience'] + "</td><td scope='col'>" + value['current_ctc'] + "</td><td scope='col'>" + value['expected_ctc'] + "</td><td scope='col'>" + value['notice_period'] + "</td><td scope='col'>" + value['updated_on'] + "</td><td scope='col' class='resume_open' id='" + value['resume_name'] + "'value='"+value['id']+"'><img src='../static/css/document-edit-icon.png' width='22px' class='changeprofile' id='"+ value['resume_name'] +"' value='"+value['id']+"' '></img></td></tr>")

                    }
                })

            }
            else {

                $('#new_profile_table_row').append('<tr>  <td colspan="10" style="text-align:  center;">No Records Found</td></tr>')
            }
      $('#unAttachedProfiles').DataTable().ajax.reload();


        }
    })
}



// atach profiles
$(document).on('click', '.attach_profiles', function(event) {
company_id = $("#dash_board_table option:selected").val();
job_id      = $("#dash_board_job  option:selected").val();


//    $('select[name ="city"]').change(function () {
//        sel_imie.prop('disabled', false);
//    });


    if (company_id == 0 ) {

            $('#select_company_profile').removeClass('hide')
  setTimeout(function(){ $('#select_company_profile').addClass('hide') }, 1000);



    }
    else if(job_id == 0){

   $('#select_job').removeClass('hide')
  setTimeout(function(){ $('#select_job').addClass('hide') }, 1000);


   }
     else{
       var com_dd = $('select[name="company_dropdown"]')
    com_dd.prop('disabled', true);
    var job_dd = $('select[name="job_dropdown"]')
    job_dd.prop('disabled', true);

     getUnattchedProfiles(job_id, company_id)

     }

})
$(document).on('click', '.attach_profiles_resume', function(event) {
company_id = $("#edit_resume_company option:selected").val();
job_id      = $("#edit_resume_job  option:selected").val();
    var resume_id = [];

    pr_id = document.getElementById("pro_id").value
 resume_id.push(pr_id);


  if (company_id == 0 ) {

            $('#select_company_resumeview').removeClass('hide')
  setTimeout(function(){ $('#select_company_resumeview').addClass('hide') }, 1000);



    }
    else if(job_id == 0){

   $('#select_job_resumeview').removeClass('hide')
  setTimeout(function(){ $('#select_job_resumeview').addClass('hide') }, 1000);


   }
     else{
          SaveAttchedProfiles(job_id, company_id, resume_id)

     }




})


$(document).on('click', '.second_layer', function(e) {

    var leng_arry = []

    $(this).parents('#new_profile_table_row').find('tr').each(function() {
        if ($(this).find('td > input[type="checkbox"]').prop('checked') == true) {
            leng_arry.push($(this).find('input[type="checkbox"]').attr('id'))
        }
    })
    profiles_id = leng_arry

})



$(document).on('click', '.save_profiles_jobs', function(e) {
job_id=document.getElementById("attach_job_id").value
company_id = document.getElementById("attach_com_id").value
            var com_dd = $('select[name="company_dropdown"]')
   com_dd.prop('disabled', false);
    var job_dd = $('select[name="job_dropdown"]')
    job_dd.prop('disabled', false);




    SaveAttchedProfiles(job_id, company_id, profiles_id)

})



function SaveAttchedProfiles(jobid, compid, profile_arr) {



    var data = {
        'profile_ids': profile_arr,
        'jobid': jobid,
        'comid': compid
    }

 $('#dashboard_details').removeClass('hide')
                        $('#dashboard_details').addClass('show')
            $('#new_profiles').removeClass('show')
            $('#new_profiles').addClass('hide')
 $('#company_dropdown').removeClass('hide')
                        $('#job_dropdown').removeClass('hide')
                         $('#company_attach').removeClass('show')
                        $('#company_attach').addClass('hide')

    $.ajax({
        data: JSON.stringify(data),
        datatype: 'JSON',
        url: "/attachprofiles/",
        method: "post",
        success: function(data) {
        console.log(data ,"asdassaasa")
        profiles_id = ""

                        dashboardLoad(compid,jobid)
                         toastr.success(data.msg)

                  document.getElementById("attach_profiles_resume").disabled = true;



        }
    })
}


//add customer

function add_customer() {
    console.log("hio");

    var first_name = document.getElementById("f_name").value;
    var last_name = document.getElementById("l_name").value;
    var email = document.getElementById("e_mail").value;
    var company_name = document.getElementById("com_name").value;
    var password = document.getElementById("mypassword").value;
    var phone_number = document.getElementById("cust_phone").value;


    $.ajax({
        url: "/operatorlist/",
        method: 'post',

        data: {
            first_name: first_name,
            last_name: last_name,
            email: email,
            company_name: company_name,
            password: password,
            phone_number: phone_number,
        },
        dataType: 'json',
        success: function(data) {
            console.log("dataaa#########", data);
            swal(data.msg);

        }
    });
}


//tabs navigation


$("#dashboard_tab").click(function() {

    if (!$(this).hasClass("active")) {


        $('#dashboard_tab').addClass('active')
        $('#profiles_tab').removeClass('active')
        $('#jobs_tab').removeClass('active')
        $('#user_tab').removeClass('active')
        $('#interview_tab').removeClass('active')

        $('#customer_tab').removeClass('active')


    }

});
$("#customer_tab").click(function() {

    if (!$(this).hasClass("active")) {


        $('#customer_tab').addClass('active')
        $('#profiles_tab').removeClass('active')
        $('#jobs_tab').removeClass('active')
        $('#user_tab').removeClass('active')
        $('#interview_tab').removeClass('active')

        $('#dashboard_tab').removeClass('active')


    }

});

$("#profiles_tab").click(function() {

    if (!$(this).hasClass("active")) {

        $(this).addClass('active')
             $('#profiles_tab').addClass('active')

        $('#customer_tab').removeClass('active')
        $('#jobs_tab').removeClass('active')
        $('#user_tab').removeClass('active')
        $('#interview_tab').removeClass('active')

       $('#dashboard_tab').removeClass('active')


    }

});


$("#interview_tab").click(function() {

    if (!$(this).hasClass("active")) {

        $(this).addClass('active')
        $('#customer_tab').removeClass('active')
        $('#profiles_tab').removeClass('active')
        $('#user_tab').removeClass('active')
        $('#dashboard_tab').removeClass('active')



    }

});

$("#user_tab").click(function() {

    if (!$(this).hasClass("active")) {

        $(this).addClass('active')
        $('#customer_tab').removeClass('active')
        $('#profiles_tab').removeClass('active')
        $('#jobs_tab').removeClass('active')
        $('#interview_tab').removeClass('active')
        $('#dashboard_tab').removeClass('active')


    }

});

//get attached profiles
 var job_id = ''

$(document).on('click', '.main_card', function(event) {
    $(this).addClass("active");
    $(this).siblings().removeClass("active");

    var id = $(this).attr('id');
     job_id = id
       console.log(job_id, "this is job id which is selected...........")
     var data={"job_id":id}

//   ajaxDataTableCall(data)

})

function getProfiles(id) {

    $.ajax({

        data: id,
        datatype: 'JSON',
        url: "/profiledetails/?jobid=" + id,
        method: "get",
        success: function(data) {
            console.log(data, "ssssssssssss")
            $('#profile_table_row').empty()
            $('#show_attached_profiles').removeClass('hide')
            $('#show_attached_profiles').addClass('show')
            $('#new_profiles').addClass('hide')
            $('#new_profiles').removeClass('show')
            $('#jobDetails').DataTable().clear().destroy();
            $('#table_id').empty();
            if (data.profiledetails.length > 0) {
                $.each(data.profiledetails, function(key, value) {

                    $('#profile_table_row').append("<tr id=" + value['resume_id'] + "> <td scope='col'>" + value['resume__candidate_name'] + " <br> " + value['resume__candidate_email'] + " <br> " + value['resume__phone_number'] + "</td><td scope='col'>" + value['resume__primary_skills'] + "</td><td scope='col'>" + value['resume__current_company'] + "</td><td scope='col'>" + value['resume__experience'] + "</td><td scope='col'>" + value['resume__current_ctc'] + "</td><td scope='col'>" + value['resume__expected_ctc'] + "</td><td scope='col'>" + value['resume__notice_period'] + "</td><td scope='col' class='resume_open' id='" + value['resume__resume_name'] + "'><i class='	fa fa-file-text-o fa-2x   editbtn_d'></i></td><td scope='col'>" + value['final_status'] + "</td><td class='get_chat' scope='col'><button>converse</button></td><td class='delete_profile' scope='col'></td></tr>")

                })
            } else {


                $('#profile_table_row').append('<tr>  <td colspan="10" style="text-align:  center;">No Records Found</td></tr>')


            }
                  $('#jobDetails').DataTable().ajax.reload();

        }
    })

}
$(document).on('change', '.dash_board_table', function(event) {
var id = $(this).val();
JoblistCall(id)
                  document.getElementById("attach_profiles_resume").disabled = false;

s_id = $("#job_status option:selected").val();
if(s_id==0){

dashboardLoad(id,0)
}
else{
dashboardLoad(id,2,s_id)
}

while(convertedData.length > 0) {
    convertedData.pop();
}
})

$(document).on('change', '.sort_by_job', function(e){
//var c_id = $('#dash_board_table .true').val();
                  document.getElementById("attach_profiles_resume").disabled = false;

c_id = $("#dash_board_table option:selected").val();

var j_id = $(this).val();


dashboardLoad(c_id, j_id)
getallstatus()

while(convertedData.length > 0) {
    convertedData.pop();
    }

})

$(document).on('change', '.job_status', function(e){
//var c_id = $('#dash_board_table .true').val();
s_id = $("#job_status option:selected").val();
c_id = $("#dash_board_table option:selected").val();
JoblistCall(c_id)

if(s_id==0){

dashboardLoad(c_id,0)
}
else{

dashboardLoad(c_id,2,s_id)

}
})
//get jobs of company
$(document).on('change', '.oncustomer', function(event) {
    $(this).addClass("active");
    $(this).siblings().removeClass("active");
    var id = $(this).val();
    company_id = id
   localStorage.setItem('com_id',$(this).val());
   var com_id=localStorage.getItem('com_id')
   console.log(com_id , "this is required")

    JoblistCall(id)

})


 $('#example').DataTable( {
        "ajax": '../ajax/data/arrays.txt'
    } );


//    for ajax data table for attached resumes


function ajaxDataTableCall(data){
                        $('#data_table_server').DataTable().clear().destroy();


                        $('#show_attached_profiles').removeClass('hide')
                         $('#show_attached_profiles').addClass('show')
                         $('#new_profiles').addClass('hide')
                         $('#new_profiles').removeClass('show')

        var dt_table = $('#data_table_server').dataTable({
        language: dt_language,  // global variable defined in html
        order: [[ 0, "desc" ]],
        lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
        columnDefs: [
            {orderable: true,
             searchable: true,
             className: "center",
            },


        ],
        searching: true,
        processing: true,
        serverSide: true,
        stateSave: true,
        data     : data,
        ajax:{
                url:'/ticket_data/',
                data: data,
            datatype: 'JSON',
            method: "GET",

            dataSrc:function(json) {

                    return json.data;
                },
        }
    });


}
$(document).ready(function() {

function checkChange($this){
var value = $this.val();

   var sv=$this.data("stored");

   if(value!=sv)
       $this.trigger("simpleChange");

}

$(this).data("stored",$(this).val());
   $("input").bind("keyup",function(e){
   checkChange($(this));
});


$("input").bind("simpleChange",function(e){
job_data_change = true
document.getElementById("savee").disabled = false;

});



$('#Mainform').on('change', function(){ // on change of state
document.getElementById("savee").disabled = false;
job_data_change = true

   });

   $('#JobStatus').on('change', function(){ // on change of state
document.getElementById("savee").disabled = false;
job_data_change = true

   });

});


// for edit and update job..........

$(document).on('click','.jobedit',function(e){

   $('#editJobModal').modal('show')
document.getElementById("savee").disabled = true;

   show_job_details(job_id)



  })


function show_job_details(job_id)
{
job_data_change = false

document.getElementById("savee").disabled = true;




   $('#editJobModal').modal('show')

document.getElementById("edit_job_id").value = job_id;
    $.ajax({
              datatype: 'JSON',
              url: "/job_details_show/?job_id="+ job_id,
              method: "get",
              success: function(data) {
              console.log(data.jobs)
               $.each(data.jobs, function(key, value){


               $('input[id="p_skills"]').val(value['primary_skills'])
               $("textarea#jobdescription").val(value['job_description']);
               $('input[id="edit_job_id"]').val(value['job_id'])
               $('input[id="exp"]').val(value['experience'])
               $('input[id="no_positions"]').val(value['no_positions'])
               $('input[id="created_for"]').val(value['created_for'])
               $('input[id="lead_time"]').val(value['lead_time'])
               $('input[id="job_title"]').val(value['job_title'])
               $('input[id="location"]').val(value['location'])
               $('input[id="date"]').val(value['job_end_date'])
               $('input[id="reference_id_update"]').val(value['reference_id'])







               if(value['job_type'] == 'full_time'){
                document.getElementById("full_time").checked = true;




                }
                else if(value['job_type'] == 'contract'){

                          document.getElementById("contract").checked = true;


                }
                else if(value['job_type'] == 'contract_hire'){

                          document.getElementById("contract_hire").checked = true;

                }
                else {

                          document.getElementById("full_time").checked = true;



                }



            if(value['job_status'] == 'Active'){

                document.getElementById("close_job").checked = false;
                document.getElementById("hold_job").checked = false;

                document.getElementById("active_job").checked = true;
                }
                else if(value['job_status'] == 'Hold'){

                document.getElementById("close_job").checked = false;
                document.getElementById("active_job").checked = false;

                document.getElementById("hold_job").checked = true;
                }
                else if(value['job_status'] == 'Closed'){

                document.getElementById("close_job").checked = true;
                document.getElementById("hold_job").checked = false;
                document.getElementById("active_job").checked = false;


                }
                else if(value['job_status'] == 'Canceled') {

                document.getElementById("cancel_job").checked = true;


                }
                else{
                   document.getElementById("active_job").checked = true;



                }



               })

              }
     });
 }





$(document).on('click', '.edit_job', function(event) {



job_id=document.getElementById("edit_job_id").value;
 var primary_skills=document.getElementById("p_skills").value;
 var job_description=document.getElementById("jobdescription").value;
 var experience=document.getElementById("exp").value;
 var no_positions=document.getElementById("no_positions").value;
 var created_for=document.getElementById("created_for").value;
 var lead_time=document.getElementById("lead_time").value;
 var reference_id=document.getElementById("reference_id_update").value;
 var location=document.getElementById("location").value;
 var job_end_date=document.getElementById("date").value;
 var job_type=document.Mainform.rds.value;
 var job_status = document.JobStatus.js.value



update_jobs(job_id,primary_skills,job_description,experience,no_positions,created_for,lead_time,reference_id,location,job_end_date,job_type,job_status)


})


function update_jobs(job_id,primary_skills,job_description,experience,no_positions,created_for,lead_time,reference_id,location,job_end_date,job_type,job_status){
console.log(job_type)
data={"job_id" : job_id , "primary_skills" : primary_skills, "job_description" : job_description ,"experience" :experience , "no_positions" :no_positions , "created_for" :created_for , "lead_time" :lead_time, "reference_id" : reference_id ,"location":location,"job_end_date":job_end_date,"job_type":job_type,"job_status":job_status}


 $.ajax({


                datatype: 'JSON',
                data : data,
                url: "/updatejob/",
                method: "post",

                success: function(data) {
                toastr.success(data.msg)

                  $('#editJobModal').modal('hide')
company_id = $("#dash_board_table option:selected").val();
job_id      = $("#dash_board_job  option:selected").val();
s_id = $("#job_status option:selected").val();

if(s_id == 0){
dashboardLoad(company_id , job_id)
}

 else{
dashboardLoad(c_id,2,s_id)

 }

          }

          });
}

$(document).on('click', '.cancell ', function(e) {
if (job_data_change == true)
{
toastr.error("Please save the changes")
}
else {
   $('#editJobModal').modal('hide')

}
})
//for logout

$(document).on('click', '.logout ', function(e) {


        localStorage.clear()
        window.location.href="/logout/"

});

//when click on profile repository to load data

$(document).on('click', '.getallprofile' , function(e){

profileRepositoryload()

});
function profileRepositoryload(){
                        $('#data_table_repository').DataTable().clear().destroy();


$.fn.dataTable.ext.errMode = 'throw';

        var dt_table = $('#data_table_repository').dataTable({
        language: dt_language,  // global variable defined in html
        order: [[ 11, "desc" ]],
         columnDefs: [
        { targets: [1], orderable: false},
           { width: "8%", targets: 0 },
      { width: "2%", targets: 1 },
      { width: "12%", targets: 2 },
      { width: "8%", targets: 3 },
      { width: "7%", targets: 4 },
      { width: "19%", targets: 5 },
      { width: "8%", targets: 6 },
      { width: "4%", targets: 7 },
      { width: "6%", targets: 8},
      { width: "6%", targets: 9 },
      { width: "5%", targets: 10 },
      { width: "7%", targets: 11 },
      { width: "7%", targets: 12 },





        ],




//        columnDefs: [
//            {
//            targets: [11],
//
//                name:  'updated_on',
//                type:  'datetime',
//                def:   function () { return new Date(); },
//                format: 'DD MM YYYY ',
//
//
//
//            },
//
//
//        ],


fields: [ {
                label:  'Last updated',
                name:   'updated_on',
                type:   'datetime',
                def:    function () { return new Date(); },
                format: 'M/D/YYYY',
                fieldInfo: 'US style m/d/y format'
            },
],
//
//    orderable: false,
        searching: true,
//        processing: true,
        serverSide: true,
        stateSave: true,

        ajax:{
                url:'/loadprofilerepository/',

            datatype: 'JSON',
            method: "GET",

            dataSrc:function(json) {

                    return json.data;
                },
        }
    });


}



$(document).ready(function() {
    var activeTab = localStorage.getItem('activeTab');
    if(activeTab == "#profile"){

    profileRepositoryload()
    }
    else{
    console.log("aaaaaaaaaaaaaaaaaaaaaaaa")
    }

    })

//hide option onchange......
$(".oncustomer").change(function ()
{
    $(" option[id='select_company']").hide();
});

//to drop dwon list and add new skilss

  jQuery(document).ready(function($) {


var data1 = [];
$.ajax({
  url : "/getallskills/",
  method : "get",
   success : function(data){

                  $.each(data.skills, function(key,value) {

                data1.push(value['skill']);
                });
    <!--for(var i = 0; i < options.length; i++) {-->
    <!--var opt = options[i];-->
    <!--var el = document.createElement("option");-->
    <!--el.textContent = opt;-->
    <!--el.value = opt;-->
    <!--select.appendChild(el);-->
<!--}-->


$(".tags_input").tagComplete({
      freeInput : true,
  freeEdit : true,

    ignoreCase: true,

  autocomplete: {
      ignoreCase: true,

    data: data1
  },
// when a new tag is added
  onAdd: function(data){
    return true;
  },

  // when a tag is deleted
  onDelete: function(data){
    return true;
  }


});

   }


});




});

$(document).ready(function(){

dashboardLoad(0,0)
getalljobs()
getallstatus()
while(convertedData.length > 0) {
    convertedData.pop();
}
});



$(document).on('click', '.getdashboardDetails' , function(e){

dashboardLoad(0,0)
getalljobs()
getallstatus()
while(convertedData.length > 0) {
    convertedData.pop();
}
});

var dashboarddetails = []
var convertedData=[];

function dashboardLoad(company_id , job_id,status_value){
while(convertedData.length > 0) {
    convertedData.pop();
}
$.ajax({
    datatype : "JSON",
    data : {"c_id" : company_id , "j_id" : job_id , "status_value": status_value },
    url : "/dashboarddetails/",
    method : "get",
    success: function(data){
     dashboarddetails = data.dashboarddetails

//     if(data.dashboarddetails.length > 0){
                 $('#dashboard_table').empty();
                converData();



    }

})


}

function converData(){

dashboarddetails.forEach((event)=>{
let temp=[]
while(temp.length > 0) {
    temp.pop();
}

Object.keys(event).forEach(function(key, idx) {
    temp.push(event[key]);
});

convertedData.push(temp)

})
renderTable()
}





function renderTable(){
// $('#dashboard_data').dataTable({}).destroy();
 table = $('#dashboard_data').removeAttr('width').DataTable({



        destroy:true,

        data: convertedData,

//         columnDefs: [
//
//
////
//      { width: "20%", targets: 0 },
//      { width: "2%", targets: 3 },
//      { width: "14%", targets: 4 },
//      { width: "7%", targets: 8 },
//      { width: "20%", targets: 9 },
//      { width: "8%", targets: 10 },
//      { width: "5%", targets: 11 },
//      { width: "5%", targets: 12 },
//      { width: "5%", targets: 13},
//      { width: "5%", targets: 14 },
//      { width: "3%", targets: 15 },
//      { width: "9%", targets: 16 },
//      { width: "3%", targets: 20 },
//


//    ],









columnDefs: [

            {

                render: function ( data, type, row ) {

                 if (row[2]==null){
                  return '<td><div class="dropdown"> <i class="fa fa-ellipsis-h fa-2x dropdown-toggle" data-toggle="dropdown" aria-hidden="true"></i> <ul class="dropdown-menu"><li><a href="#"> <i onclick="getUnattchedProfiles('+ row[17] + ', '+ row[7] +')"> Attach Profiles </i></a></li><li><a href="#"><i onclick="show_job_details('+ row[17] +')" >Edit Job</i></a></li><li><a href="#"><i onclick="delete_job('+ row[17] +')" >Delete Job</i></a></li> </ul>  </div></td>';

                }

                return '<td><div class="dropdown"> <i class="fa fa-ellipsis-h fa-2x dropdown-toggle" data-toggle="dropdown" aria-hidden="true"></i> <ul class="dropdown-menu"> <li><a href="#"><i onclick="delete_jobprofile('+ row[18] +', '+ row[17] +')"> Delete Profile </i></a></li>  </ul>  </div></td>';

                },
                targets: 3,
                 },

                 {
                render: function ( data, type, row ) {

                 if (data==null){
                  return '<td></td>';

                }
                    return '<td><select class="operator_status" id=" '+ row[18] +' " value=" '+ row[18] + '   "><option> ' +  data + '</option><option> Reject</option><option>Duplicate </option><option>First Round</option><option>Second Round</option><option>Third Round</option><option>Offered</option><option>Joined</option><option>Not intrested</option></select></td>';



                },
                targets: -5,
                 },


                {
                render: function ( data, type, row ) {
                if(row[2]==null)
                {
                                    return '<span  onclick="show_job_details('+ row[17] +')"  style="color:red;cursor:pointer;" > '+ data +' <span> </span>' + ' (' + row[3] + ')'  +' <br>  '+ row[19]+'<br>' ;

                }
                    return '<span style="cursor:pointer;"  onclick="show_job_details('+ row[17] +')"> '+ data +' <span> ' +'(' + row[3] + ')'  +' <br> <span style="color: #009dff;" >  '+ row[2]+'<br>';
                },
                targets: 0,
                 },
                 {


// "abcdefg"

                render: function ( data, type,row) {

                if(data!=null)
                {



                   var extention = data.slice((data.lastIndexOf(".") - 1 >>> 0) + 2)


                         return '<td class="resume_open" ><img id="'+ data +'" value=" '+ row[18] +' " style="cursor:pointer;" src="../static/css/document-edit-icon.png" width="22px" class="editbtn_d" title="view profile and record notes"></img></td>';





                   }

               else
                {
                   return '<td></td>'
                }


                },
                targets: 15
},
 {
                render: function ( data, type,row) {
                if(row[5] == null)
                {
                    return '<td></td>';
                    }
                else{
                        return data + '<br>'+ row[5] + '<br>' + row[6];
                                  }
                },
                targets: 4
},

 {
                render: function ( data, type,row) {
                 if(row[5] == null)
                {
                    return '<td></td>';
                    }
                else if (row[20] == 1){
                   return '<td><i class= "fa fa-comments-o - icon_xlarge clr_red"  onclick="getallmessages('+ row[17] + ', '+ row[18] +' ,'+ row[7] +')" scope="col"> </i></td>';


                }

                else{

                    return '<td><i class= "fa fa-comments-o - icon_med"  onclick="getallmessages('+ row[17] + ', '+ row[18] +' ,'+ row[7] +')" scope="col"> </i></td>';
}
                },
                targets: -1
},



            { visible: false,  targets: [ 1,2,5,6,7,17,18,-2] },
                    { targets: [3], orderable: false},



                 { width: "12%", targets: 0 },
      { width: "4%", targets: 3 },
      { width: "12%", targets: 4 },
      { width: "7%", targets: 8 },
      { width: "20%", targets: 9 },
      { width: "8%", targets: 10 },
      { width: "5%", targets: 11 },
      { width: "5%", targets: 12 },
      { width: "5%", targets: 13},
      { width: "5%", targets: 14 },
      { width: "5%", targets: 15 },
      { width: "9%", targets: 16 },
      { width: "3%", targets: 20 },


        ],



        fixedColumns: true,



        columns: [
            {  title: "Job Details" },

            {  title: "Job Title" },
            {  title: "Positions." },
            {  title  : "Action"},

            {   title: "Candidate Details" },
            {   title: "Candidate Email" },
            {  title: "Phone Number" },
            {  title: "Company id"},
            {   title: "Role"},

            {  title: "Skills" },
            {  title: " Current Company" },
            { title: "Exp" },
            {  title: "CTC" },

            {  title: "E-CTC" },
            {  title: "NP(days)"},
            { title: "Resume" },
            { title : "Status"},
            { title : "job id"},
            { title  : "id"},
            { title : "comapny_name"},
            { title : "Chat"},




        ],


})




}

$(document).on('change', '.operator_status', function(e){
var status = $(this).find(":selected").text()
  jpa_id= $(this).attr('id')
updatestatus(jpa_id,status)
    });
 function updatestatus( j_id,status){
$.confirm({
    title: '',
    content: 'Do you wish to update status?',
    buttons: {
    cancel: function () {

        },


        update: function () {



      data = {'job_id' : j_id , 'status' : status }

      $.ajax({

          data : data,
          datatype : 'JSON',
          url       :"/statusupdate/",
          method    : "post",

          success   : function(data){
                $("#statusModal").modal('hide')

                toastr.success(data.msg)

          }

          });
}



}});

      }


//
//window.onscroll = function() {myFunction()};
//
//var navbar = document.getElementById("dashboarddata");
//var sticky = navbar.offsetTop;
//
//function myFunction() {
//  if (window.pageYOffset >= sticky) {
//    navbar.classList.add("sticky")
//  } else {
//    navbar.classList.remove("sticky");
//  }
//}

function changetable(){
 $(".dashboardtables tbody").find("tr").each(function () {

 console.log($(this).html())

 console.log($(this).find('td:last').html())
 var td_value = $(this).find('td:last').html()
                     $(this).find('td:last').hide()

if(td_value=='false'){
        console.log(td_value,"only false")
                    $(this).find('td').css('background-color', '#dff0d8');
                    }


//
//
//        }
// console.log($("table:first tr td:last-child"));

//  console.log($(this).html().("tr td:nth-child(2)"))
//        //get the ID from the first TD
//        var ID = $(this).children(':first').text();
//
//        //create an array to hold the info from each TD within a TR
//        var rowInfo = new Array();
//
//        //loop through each TD in the row and add the text to the array
//        $(this).children('td').each(function() {
//            rowInfo.push($(this).text());
//        })
//        console.log(rowInfo[7] , "aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
//        if(rowInfo[7] =='false'){
//        console.log(rowInfo[7],"only false")
//                    $('td',).css('background-color', '#dff0d8');
//
//
//        }
 });
}


function getalljobs(){

$("#dash_board_job option").remove();
                   $("#dash_board_job").append('<option id="0" value="0" selected>select all</option>');

$("#dash_board_table option").remove();
$("#dash_board_table").append('<option id="0" value="0" selected>select all</option>')

    $.ajax({
        datatype: 'JSON',
        url: "/getalljobs/",
        method: "get",
        success: function(data) {
        console.log(data.jobs , "all jobs")
//                    $.each(data.jobs, function(key, value) {

//                    $("#dash_board_job").append('<option id=" ' + value['id'] + ' " value=" ' + value['id'] + ' "  >' + value["job_title"] +  ' </option>')

//});

        $.each(data.companies, function(key, value) {

                    $("#dash_board_table").append('<option id=" ' + value['id'] + ' " value=" ' + value['id'] + ' ">' + value["company_name"] + '</option>')

});

        }
    });

}


function getallstatus(){
$("#job_status option").remove();
$("#job_status").append('<option id="0" value="0" selected>select all</option>')

    $.ajax({
        datatype: 'JSON',
        url: "/alljobstatus/",
        method: "get",
        success: function(data) {
        console.log(data.status , "all jobs")


        $.each(data.status, function(key, value) {

                    $("#job_status").append('<option id=" ' + value['id'] + ' " value="' + value['status'] + '">' + value["status"] + '</option>')

});

        }
    });

}








function getallcompanylist(){

$("#edit_resume_job option").remove();
                   $("#edit_resume_job").append('<option id="0" value="0" selected>select all</option>');

$("#edit_resume_company option").remove();
$("#edit_resume_company").append('<option id="0" value="0" selected>select all</option>')

    $.ajax({
        datatype: 'JSON',
        url: "/getalljobs/",
        method: "get",
        success: function(data) {
        console.log(data.jobs , "all jobs")
//                    $.each(data.jobs, function(key, value) {

//                    $("#dash_board_job").append('<option id=" ' + value['id'] + ' " value=" ' + value['id'] + ' "  >' + value["job_title"] +  ' </option>')

//});

        $.each(data.companies, function(key, value) {

                    $("#edit_resume_company").append('<option id=" ' + value['id'] + ' " value=" ' + value['id'] + ' ">' + value["company_name"] + '</option>')

});

        }
    });

}

$(document).on('click' , '.openmodel_addjob' , function(e){
c_id = $("#dash_board_table option:selected").val();
if(c_id==0)


{

            $('#select_company').removeClass('hide')
//            $('#select_job').addClass('show')
  setTimeout(function(){ $('#select_company').addClass('hide') }, 1000);


 }

else {
    Openmodel(c_id)
    }
})




            $( function() {
    $( "#job_end_date" ).datepicker({
      changeMonth: true,
      changeYear: true,
      dateFormat:"dd-mm-yy",
      minDate: +1,
      maxDate: 45
    });
  } );




            $( function() {
    $( "#date" ).datepicker({
      changeMonth: true,
      changeYear: true,
      dateFormat:"dd-mm-yy",
      minDate: +1,
      maxDate: 45
    });
  } );
$(document).on('click' , '.create_job_oper' , function(e){

validate_job()

})

function validate_job() {
$("#createjob").validate({


              rules: {

                  "job_title": {
                      required: true,
                  },
                  "experience": {
                      required: true,
                  },
                  "no_positions": {
                      required: true,

                  },
                 "primary_skills": {
                      required: true,
                  },
                   "lead_time": {
                      required: true,
                      minlength: 1,
                      maxlength: 2
                  },
                   "created_for": {
                      required: true,

                  },
                  "location": {
                      required: true,

                  },
                  "job_type": {
                      required: true,

                  },




              },


              submitHandler: function (form) { // for demo
                  create_operator_job()
              }


              });
}



function create_operator_job()
{

    var companyid_job=document.getElementById("companyid_job").value;
    var title = document.getElementById("title").value;
    var job_end_date = document.getElementById("job_end_date").value;
    var prim_skills = document.getElementById("prim_skills").value;
    var j_desc = document.getElementById("jd").value;
    var reference_id = document.getElementById("reference_id").value;
    var loc = document.getElementById("loc").value;

    var expe = document.getElementById("expe").value;
    var no_of_pos = document.getElementById("no_of_pos").value;
    var leadtime = document.getElementById("leadtime").value;
    var createdfor = document.getElementById("createdfor").value;
    var job_type = $("input[name='job_type']:checked").val();



    var data = {
        "companyid_job":companyid_job,
        "jobtitle": title,
        "job_end_date": job_end_date,
        "primaryskills": prim_skills,
        "jobdescription": j_desc,
        "reference_id": reference_id,
        "location": loc,
        "experience": expe,
        "positions": no_of_pos,
        "leadtime":leadtime,
        "createdfor":createdfor,
         "job_type" :job_type,


    }



    $.ajax({

                 data : data,
                url: "/operatorcreatejob/",
                method: "post",
                success: function(data) {
                company_id = $("#dash_board_table option:selected").val();
                 toastr.success(data.msg)
                    dashboardLoad(company_id , 0)
                    JoblistCall(company_id)


          }

          });

                         $('input[id="prim_skills"]').val("")
document.getElementById('createjob').reset();

                     $('#create_job').modal('hide')

}

            $("#fileLoader").change(function(e){
            $.preloader.start({


                        modal: true
            });




                    var filecount=e.target.files.length


         var size=document.getElementById('fileLoader').files[0].size;
         if(size>1048576){
         toastr.error("File Size should be less than 1MB")
                       }


         else{
                   <!--var fd = new FormData($('#loader_files')[0]);-->

                   <!--var fd = new FormData();-->
                   var fd = new FormData($('#loader_files')[0]);
                   var filecount=e.target.files.length;
                   fd.append("filecount",e.target.files.length)

                   $.ajax({
                       url: "/extract-file/",
                       data:fd,
                       processData: false,
                       method: 'post',
                       contentType: false,
                       beforeSend: function(xhr) {
                       xhr.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val())
                     },

                       success: function(dat) {
                        $.preloader.stop();



                         $("#profile_data").show();
                         console.log("dataaa#########",dat);
                     <!--$("#extracteddetails").modal('show');-->

                        $.alert(dat.msg)
                         <!--$("ol").append(dat.list);-->



                        profileRepositoryload()

                         $('#profiles_tab').trigger('click')
                     },
                       error: function(error){
                          console.log("Error", error);
                       }
                   });
                   }
                   console.log("triggered",fd);
                   console.log("file",e.target.files);
   });

$(document).on('click' , '.goback' , function(e){

           var com_dd = $('select[name="company_dropdown"]')
   com_dd.prop('disabled', false);
    var job_dd = $('select[name="job_dropdown"]')
    job_dd.prop('disabled', false);


 $('#dashboard_details').removeClass('hide')
                        $('#dashboard_details').addClass('show')
            $('#new_profiles').removeClass('show')
            $('#new_profiles').addClass('hide')
 $('#company_dropdown').removeClass('hide')
                        $('#job_dropdown').removeClass('hide')
                         $('#company_attach').removeClass('show')
                        $('#company_attach').addClass('hide')

});


function open_notes_model(res_id){

data = {"resume_id" : res_id }


$.ajax({

                 data : data,
                url: "/create_notes/",
                method: "get",
                success: function(data) {
                console.log(data)
                 $.each(data.notes, function(key, value){

               $("textarea#resume_id_notes_jpa").val(value['notes']);


});



                }
                });
}

$(document).on('click', '.save_notes' ,  function(e){
resume_id = document.getElementById("pro_id").value;

notes = document.getElementById("resume_id_notes").value;

data = {"notes" : notes , "resume_id" : resume_id}

$.ajax({

                 data : data,
                url: "/create_notes/",
                method: "post",
                success: function(data) {
                toastr.success(data.msg)




                }
                });

})
$(document).on('click', '.save_notes_jpa' ,  function(e){
resume_id = document.getElementById("pro_id_jpa").value;

notes = document.getElementById("resume_id_notes_jpa").value;

data = {"notes" : notes , "resume_id" : resume_id}

$.ajax({

                 data : data,
                url: "/create_notes/",
                method: "post",
                success: function(data) {
                toastr.success(data.msg)




                }
                });

})

$(document).on('click','.opendashboard', function(e){
company_name = $(this).parents('tr').find('td:eq(0)').html()

//$('#dashboard_tab').trigger('click'); // Nothing
//$("#dash_board_table").val(4);
//company_id = $("#dash_board_table option:selected").val();
 $("#dash_board_table option:selected").val()=9

})
//
function change_drpdwn(){
//    $('#City').val('A').trigger('change');

//    $('#dash_board_table').val(9).trigger('change');


}




$(document).on('click', '.loadnextprofile', function(e){
if(profile_data_change == true){
toastr.error("Please save the changes")

}

else {
load_next = document.getElementById("row_index_repository").value;
var next_value = parseInt(load_next, 10);

console.log(typeof load_next)
next = next_value + 1;
getnextorpreviousprofile(next_profiles[next],next_profiles_id[next])
document.getElementById("row_index_repository").value = next
}
})


$(document).on('click', '.loadprevprofile', function(e){
if(profile_data_change == true){
toastr.error("Please save the changes")

}
else {
load_prev = document.getElementById("row_index_repository").value;
var prev_value = parseInt(load_prev, 10);

prev = prev_value - 1;
getnextorpreviousprofile(next_profiles[prev],next_profiles_id[prev])
document.getElementById("row_index_repository").value = prev

}
})


function getnextorpreviousprofile(file_name , p_id){


    var extention = file_name.slice((file_name.lastIndexOf(".") - 1 >>> 0) + 2)

    if (extention == "pdf") {

        var file_type = '../media/'+file_name
        $('#resume_pdf').attr('data',file_type)

        $('#resume_doc').addClass('hide')
        $('#resume_pdf').removeClass('hide')

    } else if (extention == "doc" || extention == "docx") {


        var new_file = "https://docs.google.com/gview?url=" + location.protocol + "//" + window.location.host + "/media/" + file_name + "&embedded=true"
        $('#resume_pdf').addClass('hide')
        $('#resume_doc').removeClass('hide')
        $('#resume_doc').attr('src', new_file)


    }






   data={"p_id" : p_id}
        $.ajax({
         data     : data,
         datatype : 'JSON',
         url      : "/show_profile_details/",
         method   : "get",
         success   : function(data){

               $.each(data.details, function(key, value){


               $('input[id="email_address"]').val(value['candidate_email'])
               $('input[id="experience"]').val(value['experience'])
               $('input[id="editphone"]').val(value['phone_number'])
               $('input[id="first_name"]').val(value['candidate_name'])
               $('input[id="primary_skills"]').val(value['primary_skills'])
               $('input[id="current_company"]').val(value['current_company'])
               $('input[id="current_ctc"]').val(value['current_ctc'])
               $('input[id="expected_ctc"]').val(value['expected_ctc'])
               $('input[id="notice_period"]').val(value['notice_period'])
               $('input[id="current_location"]').val(value['location'])
               $('input[id="current_role"]').val(value['current_role'])
               $("textarea#resume_id_notes").val(value['notes']);

                    $('input[id="alternate_phone_number"]').val(value['alternate_phone_number'])

               if(value['availability']=='yes'){

                $('#availability').prop('checked', true); // Checks it

              }
               else{
                 $('#availability').prop('checked', false); // Checks it

              }



})

}

});


}





function update_profile()

{


    var pro_id = document.getElementById("pro_id").value;
    var candidate_name = document.getElementById("first_name").value;
    var candidate_email = document.getElementById("email_address").value;
    var phone_number = document.getElementById("editphone").value;
    var primary_skills = document.getElementById("primary_skills").value;
    var current_company = document.getElementById("current_company").value;
    var location = document.getElementById("current_location").value;
    var experience = document.getElementById("experience").value;
    var current_ctc = document.getElementById("current_ctc").value;
    var expected_ctc = document.getElementById("expected_ctc").value;

    var notice_period = document.getElementById("notice_period").value;
    var currentrole = document.getElementById("current_role").value;

    var alter_ph_num = document.getElementById("alternate_phone_number").value;
    var interview_services_company = document.getElementById("interview_as_a_service").value;
//    var availability = $("input[name='availability']:checked").val();



  if (interview_services_company == "True")
   {

       var interviewr_skills = document.getElementById("interview_skills").value;


   var interviewr = document.getElementById("Interviewer").checked;
   if(interviewr){
    is_interviewr = "True"
   }
   else{
   is_interviewr = "False"
   }

}
  else{
         interviewr_skills = ""
            is_interviewr = "False"

      }





   var status = document.getElementById("availability").checked;

   if (status) {
      availability = "yes"
   } else {
availability = "no"

   }




    var data = {
        pro_id:pro_id,
        candidate_name: candidate_name,
        candidate_email: candidate_email,
        phone_number: phone_number,
        current_company: current_company,
        primary_skills: primary_skills,
        location: location,
        experience: experience,
        current_ctc: current_ctc,
        expected_ctc: expected_ctc,
        notice_period:notice_period,
        availability:availability,
        currentrole :currentrole,
        alter_ph_num : alter_ph_num,
        is_interviewr : is_interviewr,
        interviewr_skills : interviewr_skills,
    }



$.ajax({


                datatype: 'JSON',
                url: "/updateprofile/?pro_id=" + pro_id,
                data:data,
                method: "post",
                success: function(data) {
                toastr.success(data.msg)

            profileRepositoryload()
            profile_data_change = false

            document.getElementById("validate_profiles").disabled = true;
            document.getElementById("validate_profiles1").disabled = true;



          }

          });


//                     $('#editprofile').modal('hide')

}




$(document).on('click', '.validate_profiles', function(e){

$("#form_edit").validate({


              rules: {

                  "candidate_name": {
                      required: true,
                  },
                  "candidate_email": {
                      required: true,
                  },
                  "phone_number": {
                      required: true,

                  },
                 "primary_skills": {
                      required: true,
                  },
                   "notice_period": {
                      required: true,
                      minlength: 1,
                      maxlength: 2
                  },





              },


              submitHandler: function (form) { // for demo
                  update_profile()
              }


              });


})


function sendDashboarddata(){
$("#Mail_ids").val("")
$("#subjects").val('')
$("#details").val("")
company_id = $("#dash_board_table option:selected").val();
job_id      = $("#dash_board_job  option:selected").val();
s_id = $("#job_status option:selected").val();
 if(company_id ==0){
 toastr.error("Please select company")

 }
else if(job_id ==0){

 toastr.error("Please select job")



 }

 else{
 $('#sendmailModal').modal('show')
data = {"company_id" : company_id , "job_id" : job_id, "status_id" : s_id}

     $.ajax({
     data : data,
     url :"/jpalisttoexcel/",
     method : 'get',
     success:function(data){
 $('#excel_attach').removeClass('hide')
      $('#excel_attach').addClass('show')
  }



});


 }



}

function download_profile(p_id){

  $.ajax({
        url: "/downloadprofile/?p_id=" + p_id,
        method: 'get',
        dataType: 'json',
        success: function(data) {

            window.location.href = "../media/"+data.filename;

 /*alert(data.filename)
//    var dlnk = document.getElementById('dwnldLnk');
    dlnk = "../media/"+data.filename
    dlnk.href = pdf;

    dlnk.click();

*/



//        link ="../media/"+data.filename
//       link.href =location.protocol + "//" + window.location.host + "/media/" + data.filename ;
//link.download =location.protocol + "//" + window.location.host + "/media/" + data.filename ;

//
//       linkHref="../media/"+data.filename
//     window.open(linkHref, "_blank");

          }

          });


}


function edit_myuser(){
first_name = document.getElementById("firstname_user").value;
email = document.getElementById("email_user").value;
phone_number = document.getElementById("phone_number_user").value

    var isChecked = $("#enabled_user").is(":checked");
            if (isChecked) {
              user_status = "True"
            } else {
              user_status = "False"
            }

 user_id = document.getElementById("User_id_user").value
 data = {"first_name" : first_name , "email" : email , "phone_number" : phone_number ,  "user_id" : user_id , "user_status" : user_status}
 $.ajax({


                datatype: 'JSON',
                data : data,
                url: "/updatemyuser/",
                method: "post",

                success: function(data) {
                toastr.success(data.msg)
                window.location.reload();

 }
 });
}


//       var indexes = table.rows( {search: 'applied'} ).indexes();
//                    var currentIndex = table.row( {selected: true} ).index();
//                    var currentPosition = indexes.indexOf( currentIndex );
//
//                    alert(this.rowIndex)

// var file_name =$(this).parents('tr').next().find('.changeprofile').attr('id')
//
//
//    var extention = file_name.slice((file_name.lastIndexOf(".") - 1 >>> 0) + 2)
//
//    if (extention == "pdf" ||extention == "pdf " || extention == " pdf"  ) {
//        var file_type = '../media/'+file_name
//        $('#viewResume_pdf').attr('data', file_type)
//
//        $('#viewResume_doc').addClass('hide')
//        $('#viewResume_pdf').removeClass('hide')
//
//         }else if(extention == "doc" ||extention == "docx" ){
//
//
//        var new_file = "https://docs.google.com/gview?url=" + location.protocol + "//" + window.location.host + "/media/" + file_name + "&embedded=true"
//        $('#viewResume_pdf').addClass('hide')
//        $('#viewResume_doc').removeClass('hide')
//        $('#viewResume_doc').attr('src', new_file)
//
//
//

$(document).on('click', '.edit_myuser' , function(e){
 user_id = document.getElementById("User_id_user").value
data = {"user_id" : user_id}
 $.ajax({


                datatype: 'JSON',
                data : data,
                url: "/checkprimaryuser/",
                method: "get",

                success: function(data) {
console.log(data)

               $.each(data.user, function(key, value){
               console.log(value['primary_user'])
            if(value['primary_user'] == false){

//                $("input.enabled_user").attr("disabled", true);
                    $('#check_box').removeClass('show')

                    $('#check_box').addClass('hide')


                     }
            else if (user_id == data.user_id) {
                    $('#check_box').removeClass('show')

                    $('#check_box').addClass('hide')


//               $("input.enabled_user").attr("disabled", true);

            }

             else {
//                 $("input.enabled_user").removeAttr("disabled");

                    $('#check_box').removeClass('hide')

                                    $('#check_box').addClass('show')


             }

               });
                $.each(data.user_active, function(key, value){




               if(value['is_active'] == false){
            $("#enabled_user").prop( "checked", false );



             }

             else {
                         $("#enabled_user").prop( "checked", true );

             }



               });


 }
 });



})

function load_interview_tab(){
window.location.reload()

}

//$(document).on('click', '.tag_complete .tags_container .tag' , function(e){
//                     alert()
//                       $(".tag_complete .tags_container .close:after").css("display", "block");
//
//                     })
//$(document).ready(function(){
//
//$(".tag_complete .tags_container .tag").mouseover(function(){
//alert()
//  $(".tag_complete .tags_container .tag .close").css("display", "block !important");
//});
//});