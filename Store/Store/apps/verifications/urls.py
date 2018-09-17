from django.conf.urls import url

from verifications import views

urlpatterns = [
    url(r'^verificationstest$', views.VerificationsTest.as_view()),
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})$', views.SMSCodeView.as_view()),
]