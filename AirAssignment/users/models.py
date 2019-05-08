from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    type = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=8)
    users = models.ManyToManyField(UserProfile, null=True)

    def __str__(self):
        return self.name


class Assignment(models.Model):
    name = models.CharField(max_length=50)
    deadline = models.DateTimeField
    course = models.ForeignKey(Course, null=True)

    def __str__(self):
        return self.name


# TODO: Migrate and add submission to admin.py
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment)
    user = models.ForeignKey(UserProfile)
    grade = models.IntegerField

