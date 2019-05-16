///* profile extraction */
//   $("#fileLoader").change(function(e){
//var size=document.getElementById('fileLoader').files[0].size;
//if(size>1048576){
//toastr.error("File Size should be less than 1MB")
//
//$('#fileLoader').val("");
//}
//
//else{
//          var fd = new FormData();
//          fd.append('file', document.getElementById('fileLoader').files[0]);
//
//          $.ajax({
//              url: '{% url 'extract-file' %}',
//              data:fd,
//              processData: false,
//              type: 'POST',
//              contentType: false,
//              beforeSend: function(xhr) {
//              xhr.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val())
//            },
//
//              success: function(data) {
//
//                $("#profile_data").load(window.location + " #profile_data")
//
//                console.log("dataaa#########",data);
//                $.each(data, function(key, value) {
//
//                    $("#profile_data").append("<tr><td></td><td>  </td><td>" + value['email'] + "</td> <td>" + value['phone'] + "</td> <td></td> <td></td> <td></td> <td></td> <td></td> <td></td>   </tr>")
//                      $('#profile_data').html(data);
//
//                })
//
//            },
//
//
//              error: function(error){
//                 console.log("Error", error);
//              }
//          });
//          }
//          console.log("triggered",fd);
//          console.log("file",e.target.files);
//
//});
//
//var cbx = $("#att"),
//    button = $("#but");
//
//cbx.click(function() {
//    button.attr("disabled", !checkboxes.is(":checked"));
//});
//
//
