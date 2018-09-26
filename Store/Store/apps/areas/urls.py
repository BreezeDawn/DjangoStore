from django.conf.urls import url

from areas import views

urlpatterns = [
    # 本应用测试接口
    url(r'^areastest$',views.AreasTestView.as_view()),
    # 省级
    url(r'^areas/$',views.ProvincesView.as_view()),
    # 市级/区级
    url(r'^areas/(?P<city_id>\d+)/$',views.CityView.as_view()),
]