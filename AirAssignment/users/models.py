from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    type = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=8, unique=True)
    users = models.ManyToManyField(UserProfile, null=True)

    def __str__(self):
        return self.name


class Assignment(models.Model):
    # TODO: Set PK (name = unique?/course with name?)
    name = models.CharField(max_length=50)
    deadline = models.DateTimeField(auto_now_add=False, editable=True, default=datetime.now())
    course = models.ForeignKey(Course)

    def __str__(self):
        return self.name


def get_submission_path(instance, filename):
    """Creates file directory path based on course and assignment."""
    _, extension = filename.split('.')
    return 'static/assignments/' \
           + instance.assignment.course.code + '/' \
           + instance.assignment.name + '/' \
           + instance.user.user.username \
           + '.' + extension


class Submission(models.Model):
    # TODO: Delete doesn't the files from static directory
    assignment = models.ForeignKey(Assignment)
    user = models.ForeignKey(UserProfile)
    grade = models.IntegerField(null=True, blank=True)
    file = models.FileField(null=True, upload_to=get_submission_path)

    class Meta:
        unique_together = (('assignment', 'user'),)

    def __str__(self):
        return self.user.user.username + "'s " + self.assignment.name + " Submission"
