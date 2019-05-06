from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password', 'email')


class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('type',)
