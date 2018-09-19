from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^userstest$', views.UsersTest.as_view()),
    url(r'^usernames/(?P<username>.*)/count/$', views.UsersCount.as_view()),
    url(r'^mobiles/(?P<mobile>.*)/count/$', views.MobilesCount.as_view()),
]