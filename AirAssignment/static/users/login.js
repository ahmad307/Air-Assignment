$('#login_form').on('submit', function (e) {
    e.preventDefault();
    $.ajax({
        url: '/users/login',
        type: 'POST',
        data: {
            'username': $('#username').val(),
            'password': $('#password').val(),
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function () {
            window.location.href = '/users/index';
        },
        error: function () {
            window.alert("Invalid Info!");
        }
    });
});