from django.shortcuts import render, HttpResponse, Http404
from django.http import FileResponse
from users import forms, models, helper
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, PermissionDenied
from django.db.utils import IntegrityError
from datetime import datetime
import json


def index(request):
    return render(request, 'index.html')


def get_index(request):
    """Returns index page for a certain user."""
    username = request.GET['name']
    courses = helper.get_courses(username)
    request.session['courses'] = list(courses)

    user_type = models.UserProfile.objects.get(user__username=username).type
    request.session['user_type'] = user_type

    request.session.modified = True
    return render(request, 'index.html')


def register(request):
    """Returns registration page and adds a new user to database."""
    if request.method != 'POST':
        return render(request, 'register.html')

    user_form = forms.UserForm(request.POST)
    profile_form = forms.UserProfileForm(request.POST)

    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        user.set_password(user.password)
        user.save()

        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()

    # Log the new user in
    return login(request)


def login(request):
    """Returns login page."""
    if request.method != 'POST':
        return render(request, 'login.html')

    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)

    if user:
        # Check if user account is active
        if user.is_active:
            auth.login(request, user)

            courses = helper.get_courses(user.username)
            request.session['courses'] = list(courses)

            user_type = models.UserProfile.objects.get(user=user).type
            request.session['user_type'] = user_type

            request.session.modified = True
            return render(request, 'index.html')
        else:
            return HttpResponse('Inactive account.')
    else:
        return Http404('Invalid Info.')


@login_required
def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


def course(request):
    """Returns course page given its name and returns its assignments list."""
    course_name = request.GET['course_name']
    assignments = helper.get_assignments(course_name)

    request.session['assignments'] = list(assignments)
    request.session['course_name'] = course_name
    request.session['course_code'] = models.Course.objects.get(name=course_name).code

    username = request.GET['username']
    user_type = models.UserProfile.objects.get(user__username=username).type
    request.session['user_type'] = user_type

    request.session.modified = True
    return render(request, 'course.html')


def assignment_instructor(request):
    """Returns an instructor's assignment page with all student submissions."""
    assignment_name = request.GET['name']
    course_name = request.GET['course']

    # Match submission with assignment object to avoid overlapping
    # assignment names
    assignment = models.Assignment.objects.get(name=assignment_name,
                                               course__name=course_name)
    submissions = models.Submission.objects.filter(assignment=assignment)

    submission_response = []
    for submission in submissions:
        submission_response.append({
             'username': submission.user.user.username,
             'grade': submission.grade})

    request.session['submissions'] = submission_response
    request.session['assignment_name'] = assignment_name
    request.session.modified = True
    return render(request, 'assignment_instructor.html')


def join_course(request):
    """Adds a student to a course given student username and course code."""
    username = request.POST['username']
    course_code = request.POST['course_code']
    course_object = models.Course.objects.get(code=course_code)
    user_object = models.UserProfile.objects.get(user__username=username)

    if user_object.type != 'student':
        return Http404

    course_object.users.add(user_object)
    course_object.save()
    return HttpResponse(json.dumps({'message': 'success'}),
                        content_type='application/json')


def add_assignment(request):
    """Saves an assignment given its info and course."""
    assignment_name = request.POST['assignment_name']
    assignment_deadline = request.POST['assignment_deadline']
    course_name = request.POST['course_name']
    course = models.Course.objects.get(name__exact=course_name)

    try:
        assignment = models.Assignment.objects.create(
            name=assignment_name,
            deadline=datetime.strptime(assignment_deadline, '%Y-%m-%d'),
            course=course)
    except IntegrityError:
        raise ValidationError('Assignment name used')
    assignment.save()

    return HttpResponse('ok')


def add_course(request):
    """Adds a new course given name and instructor username."""
    user_name = request.POST['username']
    user_in_db = models.UserProfile.objects.get(user__username=user_name)
    # Ensure course is added by an instructor
    if user_in_db.type != 'instructor':
        return Http404("Invalid User Type")

    course_name = request.POST['course_name']
    course_code = helper.get_next_course_code()

    if models.Course.objects.all().filter(code=course_code):
        return Http404('Unique Constraint Violated.')

    course_in_db = models.Course.objects.create(name=course_name, code=course_code)
    course_in_db.users.add(user_in_db)
    course_in_db.save()

    return HttpResponse(json.dumps({'code': course_code}),
                        content_type='application/json')


def get_submission_file(request):
    # TODO: Suddenly stopped working, returns empty pdf
    course_code = request.GET['code']
    assignment = request.GET['assignment']
    username = request.GET['username']
    path = 'static/assignments/' + course_code \
           + '/' + assignment + '/' + username + '.pdf'

    return FileResponse(open(path, 'rb'), content_type='application/pdf')


def add_submission(request):
    file = request.FILES['submissionFile']
    username = request.POST['username']
    assignment_name = request.POST['assignmentName']
    course_name = request.POST['courseName']

    assignment = models.Assignment.objects.get(name=assignment_name,
                                               course__name=course_name)
    user = models.UserProfile.objects.get(user__username=username)

    try:
        submission = models.Submission.objects.create(assignment=assignment,
                                                      user=user,
                                                      file=file)
    except IntegrityError:
        return HttpResponse('Submission already existing for this assignment')
    submission.save()

    return HttpResponse('Submission Added')
