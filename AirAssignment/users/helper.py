from users import models


def get_courses(username):
    """Returns name and code list of the given user's courses."""
    courses = models.Course.objects.filter(users__user__username=username).values('name', 'code')
    return courses


def get_assignments(course_name):
    """Returns a list of assignments names given their course."""
    assignments = models.Assignment.objects.all().filter(course__name=course_name).values('name')
    return assignments


def get_next_course_code():
    """Gets next available course code."""
    return int(models.Course.objects.latest('code').code) + 1
