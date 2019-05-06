from django.shortcuts import render, HttpResponse, redirect
from users import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import json


def index(request):
    return render(request, 'index.html', {'registered': False,
                                          'user_form': forms.UserForm,
                                          'profile_form': forms.UserProfileForm},)


def register(request):
    """Adds a new user by saving and linking User and UserProfile forms."""
    user_form = forms.UserForm(request.POST)
    profile_form = forms.UserProfileForm(request.POST)

    registered = False
    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        user.set_password(user.password)
        user.save()

        profile = profile_form.save(commit=False)
        profile.User = user
        profile.save()
        registered = True

    return render(request, 'index.html', {'registered': registered})


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
            # TODO: Direct user to profile
            print('Logged the guy in..!')
            return HttpResponse(json.dumps({'message': 'success'}),
                                content_type='application/json')
        else:
            return HttpResponse('Inactive account.')
    else:
        return HttpResponse(json.dumps({'error': 'Invalid Login Info.'}),
                            content_type='application/json')


@login_required
def logout(request):
    auth.logout(request)
    return render(request, 'index.html')