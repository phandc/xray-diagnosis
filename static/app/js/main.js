$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#resultform').hide()
    $('#btn-add_pred').hide()
    $('#successAlert').hide()



    // Upload Preview
    function showTherapy(data) {


        if(data == 'bacteria'){

            $('#therapy').text("Suggestion treatment for bacterial pneumonia:\n" +
                "+ Antibiotic.\n" +
                "+ Additional medications such as over-the-counter (OTC) drugs to ease aches and pains, as well as reducing fever.\n" +
                "+ Home care will often include rest and drinking plenty of fluids. \n" +
                "+ Be sure to finish a course of antibiotic therapy according to the doctor’s prescription, even if symptoms have improved.\n" +
                "+ As a precaution, those who have an increased risk of complications, include people over 65 years or under 2 months of age may also benefit from admission to enable closer monitoring.\n" +
                "\n")

        }
        else if(data == 'virus'){
             $('#therapy').text("Suggestion treatment for virus pneumonia:\n" +
                 '+ Antiviral drugs.\n' +
                 '+ Plenty of rest.\n' +
                 '+ Drink fluid, take OTC medicines to ease fever and pain.\n' +
                 '+ Go to hospital if had chest pain or difficult breathing.')
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

       $('#therapy').text('')
        $('#btn-add_pred').hide()

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
                $('#resultform').show()

                $('#btn-add_pred').show()
            },
        });
    });



    $('#btn-add_pred').click(function () {

        $.ajax({
            data: {
                predict : $('#result').val(),
                suggestion   : $('#therapy').val()
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
