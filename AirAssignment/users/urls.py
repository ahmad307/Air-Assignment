from django.conf.urls import url
from users import views

app_name = 'users'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^course', views.course, name='course'),
    url(r'^get_courses', views.get_courses, name='get_courses'),
    url(r'^join_course', views.join_course, name='join_course')
]
