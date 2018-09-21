from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^userstest$', views.UsersTestView.as_view()),
    url(r'^users/$', views.UsersRegisterView.as_view()),
    url(r'^usernames/(?P<username>.*)/count/$', views.UsersCountView.as_view()),
    url(r'^mobiles/(?P<mobile>.*)/count/$', views.MobilesCountView.as_view()),
]