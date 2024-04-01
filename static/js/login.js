$(document).ready(function() {
    $('form').submit(function(event) {
        let formData = {
            email: $('.input_email').val(),
            password: $('.input_password').val()
        };

        $.ajax({
            type: 'POST',
            url: '/auth/login',
            data: formData,
            dataType: 'json'
        }).done(function(response) {
            $('.flash-container').html('<ul class="flash-messages"><li>' + response.message + '</li></ul>');

            if(response.status === 'success') {
                setTimeout(function() {})
                window.location.href = '/generate';
            } 3000;
        }).fail(function(err) {
            console.log(err);
            $('.flash-container').html('<ul class="flash-messages"><li>There was a problem with the request. Please try again.</li></ul>');
        });

        event.preventDefault();
    });
});
