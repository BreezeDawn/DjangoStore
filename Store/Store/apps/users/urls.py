from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from users import views

urlpatterns = [
    # 本应用测试接口
    url(r'^userstest$', views.UsersTestView.as_view()),
    # 用户注册视图
    url(r'^users/$', views.UsersRegisterView.as_view()),
    # jwt自有的登录视图
    url(r'^authorizations/$', obtain_jwt_token),
    # 用户名数量查询视图
    url(r'^usernames/(?P<username>.*)/count/$', views.UsersCountView.as_view()),
    # 手机号数量查询视图
    url(r'^mobiles/(?P<mobile>.*)/count/$', views.MobilesCountView.as_view()),
]