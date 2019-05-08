from django.shortcuts import render, HttpResponse, Http404
from users import forms, models
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import json
from django.core.serializers.json import DjangoJSONEncoder


def index(request):
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
    assignments = get_assignments(request.GET['course_name'])
    request.session['assignments'] = list(assignments)
    request.session.modified = True
    return render(request, 'course.html')

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
    course_in_db = models.Course.objects.get(name__exact=course_name)
    assignment_in_db = models.Assignment.objects.create(name=assignment_name, deadline=assignment_deadline,
                                                        course=course_in_db)
    assignment_in_db.save()


def get_assignments(course_name):
    """Returns a list of assignments names given their course."""
    assignments = models.Assignment.objects.all().filter(course__name=course_name).values('name')
    return assignments
