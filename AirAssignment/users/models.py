from django.db import models
from django.contrib.auth.models import User


class Assignment(models.Model):
    Name = models.CharField(max_length=50)
    Deadline = models.DateTimeField

    def __str__(self):
        return self.Name


class Course(models.Model):
    Name = models.CharField(max_length=50)
    Code = models.CharField(max_length=8)
    Assignments = models.ManyToManyField(Assignment)

    def __str__(self):
        return self.Name


class UserProfile(models.Model):
    User = models.OneToOneField(User)
    type = models.CharField(max_length=10, null=False)
    Courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.User.username


# TODO: Migrate and add submission to admin.py
class Submission(models.Model):
    Assignment = models.ForeignKey(Assignment)
    User = models.ForeignKey(UserProfile)
    Grade = models.IntegerField

