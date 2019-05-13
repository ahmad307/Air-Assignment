from django.shortcuts import render, HttpResponse, Http404
from users import forms, models
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime


def index(request):
    return render(request, 'index.html')


def get_index(request):
    """Returns the index page for a certain user."""
    username = request.GET['name']
    courses = get_courses(username)
    request.session['courses'] = list(courses)

    user_type = models.UserProfile.objects.get(user__username=username).type
    request.session['user_type'] = user_type

    request.session.modified = True
    return render(request, 'index.html')


def register(request):
    """Adds a new user by saving and linking User and UserProfile forms."""
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
    if request.method != 'POST':
        return render(request, 'login.html')

    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)

    if user:
        # Check if user account is active
        if user.is_active:
            auth.login(request, user)

            courses = get_courses(user.username)
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
    """Redirects to course page given its name and returns its assignments list."""
    course_name = request.GET['course_name']
    assignments = get_assignments(course_name)

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
    request.session.modified = True
    return render(request, 'assignment_instructor.html')


"""
Helper Methods
"""

def get_courses(username):
    """Returns name and code list of the given user's courses."""
    courses = models.Course.objects.filter(users__user__username=username).values('name', 'code')
    return courses


def join_course(request):
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

    assignment = models.Assignment.objects.create(
        name=assignment_name,
        deadline=datetime.strptime(assignment_deadline, '%Y-%m-%d'),
        course=course)
    assignment.save()

    return HttpResponse('ok')


def get_assignments(course_name):
    """Returns a list of assignments names given their course."""
    assignments = models.Assignment.objects.all().filter(course__name=course_name).values('name')
    return assignments


def get_next_course_code():
    return int(models.Course.objects.latest('code').code) + 1


def add_course(request):
    user_name = request.POST['username']
    user_in_db = models.UserProfile.objects.get(user__username=user_name)
    # Ensure course is added by an instructor
    if user_in_db.type != 'instructor':
        return HttpResponse("Invalid User Type")

    course_name = request.POST['course_name']
    course_code = get_next_course_code()

    if models.Course.objects.all().filter(code=course_code):
        return HttpResponse('Unique Constraint Violated.')

    course_in_db = models.Course.objects.create(name=course_name, code=course_code)
    course_in_db.users.add(user_in_db)
    course_in_db.save()

    return HttpResponse(json.dumps({'code': course_code}),
                        content_type='application/json')
