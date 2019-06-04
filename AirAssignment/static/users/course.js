$(document).ready(function () {
    $('#addAssignmentBtn').on('click', function () {
        $.ajax({
            url: '/users/add_assignment',
            type: 'POST',
            data: {
                'assignment_name': $('#assignmentName').val(),
                'course_name': $('#courseName').val(),
                'assignment_deadline': $('#assignmentDeadline').val(),
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function () {
                $('#cancelAdd').click();
                window.alert('Assignment Added.');
                window.location.href = '/users/course?' +
                                        'course_name=' +
                                        $('#courseName').val() +
                                        '&username=' +
                                        $('#username').val();
            },
            error: function () {
                window.alert('Invalid info.');
            }
        });
    });
});
