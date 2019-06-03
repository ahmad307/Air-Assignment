from django.conf.urls import url
from users import views, helper

app_name = 'users'

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^get_index', views.get_index, name='get_index'),
    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^course', views.course, name='course'),
    url(r'^assignment_instructor', views.assignment_instructor, name='assignment_instructor'),
    url(r'^get_courses', helper.get_courses, name='get_courses'),
    url(r'^join_course', views.join_course, name='join_course'),
    url(r'^add_assignment', views.add_assignment, name='add_assignment'),
    url(r'^add_course', views.add_course, name='add_course'),
    url(r'^get_submission_file', views.get_submission_file, name='get_submission_file'),
    url(r'^add_submission', views.add_submission, name='add_submission')
]
