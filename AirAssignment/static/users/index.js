function getCourses(){
    /* Not Used */
    $.ajax({
        url: '/users/get_courses',
        type: 'GET',
        data: {'username': $('#username').val()},
        success: function (json) {
            console.log(json);
            let courses = json["courses"];
            for (let i = 0; i < courses.length; i++){
                const hiddenField = "<input id='" + i +"' value='" +
                    courses[i]['code'] + "' hidden>";
                const hField = "<a href='#' id=" + i + ">" + courses[i]['name'] + "</a>";
                $('#courses_div').append(hiddenField);
                $('#courses_div').append(hField);
                $('#courses_div').append("<br><br>");
            }
        },
        error: function () {
            console.log("Error!");
        }
    })
}

$(document).ready(function () {
    $('#joinCourseBtn').on('click', function () {
        const code = $('#courseCode').val();
        $.ajax({
            url: '/users/join_course',
            type: 'POST',
            data: {
                'username': $('#username').val(),
                'course_code': code,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function () {
                $('#cancelJoin').click();
                window.alert('Course Joined.');
                window.location.href = '/users/get_index?name=' + $('#username').val();
            },
            error: function () {
                window.alert('Invalid Info.');
            }
        });
    });

    $('#addCourseBtn').on('click', function () {
        $.ajax({
            url: '/users/add_course',
            type: 'POST',
            data: {
                'username': $('#username').val(),
                'course_name': $('#courseName').val(),
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (json) {
                console.log("Success");
                $('#cancelAdd').click();
                window.alert('Course Added.\n' + 'Code: ' + json['code']);
                window.location.href = '/users/get_index?name=' + $('#username').val();
            },
            error: function (e) {
                console.log(e);
                window.alert('Invalid Info.');
            }
        });
    });
});
