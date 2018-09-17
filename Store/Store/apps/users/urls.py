from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^userstest$', views.UsersTest.as_view()),
]