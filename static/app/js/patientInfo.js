$(document).ready(function () {
     $('#successAlert').hide()




     $('#btn-add_pred').click(function () {

           $.ajax({
            data: {
                predict : $('#result').val(),
                suggestion   : $('#therapy').val()
            }
            ,
            type: 'POST',
            url: '/doctor/savepatientinfo'

        })
            .done(function (data) {
                if(data.error) {
                    // $('#errorAlert').text(data.error).show();
                    $('#successAlert').hide()
                }
                else {
                      $('#successAlert').text("Save Successful!").show().fadeOut(1000)

                      // $('#errorAlert').hide()

                }

            })

     })
})