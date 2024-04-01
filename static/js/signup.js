$(document).ready(function() {
    $('form').submit(function(event) {
        let formData = {
            email: $('.input_email').val(),
            password: $('.input_password').val(),
            firstname: $('.input_fname').val(),
            lastname: $('.input_lname').val()
        };

        $.ajax({
            type: 'POST',
            url: '/auth/signup',
            data: formData,
            dataType: 'json'
        }).done(function(response) {
            $('.flash-container').html('<ul class="flash-messages"><li>' + response.message + '</li></ul>');

            if(response.status === 'success') {
                window.location.href = '/log-in';
            }
        }).fail(function(err) {
            console.log(err);
            $('.flash-container').html('<ul class="flash-messages"><li>There was a problem with the request. Please try again.</li></ul>');
        });

        event.preventDefault();
    });
});
