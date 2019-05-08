from django.shortcuts import render, HttpResponse, Http404
from users import forms, models
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import json


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


def get_courses(username):
    user = models.User.objects.all().filter(username=username)
    user = models.UserProfile.objects.all().filter(user=user)
    print(user.Courses)
    return user.Courses


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
            #courses = get_courses(user.username)
            return render(request, 'index.html')
        else:
            return HttpResponse('Inactive account.')
    else:
        return Http404('Invalid Info.')


@login_required
def logout(request):
    auth.logout(request)
    return render(request, 'login.html')