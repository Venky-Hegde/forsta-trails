
$(document).ready(function() {

dashboardLoad(0)
getalljobs()

});
$(document).on('click', '.getdashboardDetailsCustomer' , function(e){
dashboardLoad(0)
getalljobs()

})


var dashboarddetails = []
var convertedData=[];

function dashboardLoad(job_id){
while(convertedData.length > 0) {
    convertedData.pop();
}
$.ajax({
    datatype : "JSON",
    data : { "j_id" : job_id },
    url : "/dashboarddetails/",
    method : "get",
    success: function(data){
     dashboarddetails = data.dashboarddetails
    console.log(data, "this is dataaaaa")
//     if(data.dashboarddetails.length > 0){
                 $('#dashboard_table_customer').empty();
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

 table = $('#dashboard_data_customer').dataTable({


        destroy:true,


        data: convertedData,

columnDefs: [

            {

                render: function ( data, type, row ) {


                    if (row[2]==null){
                  return '<td><div class="dropdown"> <i class="fa fa-ellipsis-h fa-2x dropdown-toggle" data-toggle="dropdown" aria-hidden="true"></i> <ul class="dropdown-menu"><li><a href="#"><i onclick="show_job_details('+ row[17] +')" >Edit Job</i></a></li><li><a href="#"><i onclick="delete_job('+ row[17] +')" >Delete Job</i></a></li> </ul>  </div></td>';

                }
                else {
                return '';

                }

                },
                targets: 3,
                 },

                 {
                render: function ( data, type, row ) {

                 if (data==null){
                  return '<td></td>';

                }
                    return '<td><select class="operator_status" id=" '+ row[18] +' " value=" '+ row[18] + '   "><option> ' +  data + '</option><option> Reject</option><option>Duplicate </option><option>First Round</option><option>Second Round</option><option>Third Round</option><option>Offered</option><option>Joined</option></select></td>';

//                     return '<td > <span class="cursor" onclick="openstatusModal(' + row[18] + ')"> '+ data +' </span> </td>'

                },
                targets: -6,
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
                    console.log(row[21], "kkkkkkkk")
                    if(row[21]== true ){
                                            return data;

                    }else{
                        console.log("here")
                        return '<td><span style="color:green">'+ data +'</span></td>';
                                 } }
                },
                targets: 4
},

 {
                render: function ( data, type,row) {
                 if(row[5] == null)
                {
                    return '<td></td>';
                    }
                else if (row[20] == 2){
                   return '<td><i class= "fa fa-comments-o - icon_xlarge clr_red"  onclick="getallmessages('+ row[17] + ', '+ row[18] +' ,'+ row[7] +')" scope="col"> </i></td>';


                }

                else{

                    return '<td><i class= "fa fa-comments-o - icon_med"  onclick="getallmessages('+ row[17] + ', '+ row[18] +' ,'+ row[7] +')" scope="col"> </i></td>';
}
                },
                targets: -2
},



            { visible: false,  targets: [ 1,2,5,6,7,17,18,-3,-1] }
        ],







        columns: [
            { title: "Job Details" },

            {   title: "Job Title" },
            {  title: "Positions." },
            { title  : "Action"},

            {   title: "Candidate Details" },
            {  title: "Candidate Email" },
            {  title: "Phone Number" },
            { title: "Company id"},
            {  title: "Role"},

            {  title: "Skills" },
            {  title: " Current Company" },
            { title: "Exp" },
            {  title: "CTC" },

            {  title: "E-CTC" },
            { title: "NP(days)"},
            { title: "Resume" },
            { title : "Status"},
            {  title : "job id"},
            { title  : "id"},
            { title : "comapny_name"},
            { title : "Chat"},
            {title  : "customer_checked"},




        ],


})




}


 function openstatusModal(jpa_id){
$("#statusModal").modal("show")
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
                    $.each(data.jobs, function(key, value) {

                    $("#dash_board_job").append('<option id=" ' + value['id'] + ' " value=" ' + value['id'] + ' "  >' + value["job_title"] +  ' </option>')

});

        $.each(data.companies, function(key, value) {

                    $("#dash_board_table").append('<option id=" ' + value['id'] + ' " value=" ' + value['id'] + ' ">' + value["company_name"] + '</option>')

});

        }
    });

}


$(document).on('click' , '.openmodel_addjob' , function(e){

    Openmodel()

})



function Openmodel() {


        $('#create_job').modal('show')

}


$(document).on('change', '.sort_by_job', function(e){
//var c_id = $('#dash_board_table .true').val();
j_id = $("#dash_board_job option:selected").val();

dashboardLoad(j_id)
while(convertedData.length > 0) {
    convertedData.pop();
    }

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



          }

          });
}
}

});
    }
}
          });





            dashboardLoad(0)
            getalljobs()


}

function show_job_details(job_id)
{
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
//               $('input[name="rds"]').val(value['job_type'])




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
job_id      = $("#dash_board_job  option:selected").val();

dashboardLoad(job_id)

          }

          });
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



function getallmessages(job_id,jpa_id ,company_id) {

    $('#messageModal').modal('show')

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
    com_id  =  company_id
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

            console.log(data)
            $('.msg_card_body').append('<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + chat + '<span class="msg_time_send">9:10 AM, </span></div><div class="img_cont_msg"><i class="fa fa-user-o" aria-hidden="true"></i></div></div>')
            $('#text_msg_value').val('')
            $(".cardsd").animate({
                scrollTop: $(document).height()
            }, 1000);

        }
    })

}
