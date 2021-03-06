from django.conf.urls import url
from rest_framework import routers
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
    # 获取用户信息
    url(r'^user/$', views.UserDetailView.as_view()),
    # 修改邮箱
    url(r'^email/$', views.EmailView.as_view()),
    # 邮箱验证
    url(r'^emails/verification/$', views.EmailVerifyView.as_view()),

]

router = routers.DefaultRouter()
router.register(r'addresses', views.AddressViewSet, base_name='addresses')

urlpatterns += router.urls
# POST /addresses/ 新建  -> create
# PUT /addresses/<pk>/ 修改  -> update
# GET /addresses/  查询  -> list
# DELETE /addresses/<pk>/  删除 -> destroy
# PUT /addresses/<pk>/status/ 设置默认 -> status
# PUT /addresses/<pk>/title/  设置标题 -> title