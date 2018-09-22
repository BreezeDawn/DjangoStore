from django.conf.urls import url

from QQ import views

urlpatterns = [
    # 本应用测试接口
    url(r'^qqtest$',views.QQTestView.as_view()),
    url(r'^qq/authorization/$',views.QQLoginView.as_view()),
]