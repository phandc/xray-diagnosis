$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();
    $('#btn-add_pred').hide()
    $('#successAlert').hide()



    // Upload Preview
    function showTherapy(data) {


        if(data == 'bacteria'){

            $('#therapy').append('<li>Just treatment at home</li>')

        }
        else if(data == 'virus'){
             $('#therapy').append('<li>Go to hospital</li>')
        }

    }
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {

        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();

        readURL(this);
          var lis = document.querySelectorAll('#therapy li');
         for(var i=0; li=lis[i]; i++) {
            li.parentNode.removeChild(li);
         }
    });

    // Predict
    $('#btn-predict').click(function () {



        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();
        console.log('goto here!')

        // Make prediction by calling api /admin/predict
        $.ajax({
            type: 'POST',
            url: '/admin/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();


                $('#result').fadeIn(600);
                // $('#result').text(' Result : ' + data);

                document.getElementById('result').value = 'Result : ' + data
                showTherapy(data)
                $('#therapy').show()


                $('#btn-add_pred').show()
            },
        });
    });



    $('#btn-add_pred').click(function () {

        $.ajax({
            data: {
                predict : $('#result').val()
            }
            ,
            type: 'POST',
            url: '/admin/addpredict'

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



});
