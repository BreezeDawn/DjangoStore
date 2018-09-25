from django.core.mail import send_mail

from celery_tasks.main import celery_app
from django.conf import settings



@celery_app.task(name='send_verify_email')
def send_verify_email(email,verify_url):
    print('发送邮件被调用')
    subject = "Story邮箱验证"
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用Story。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)
    send_mail(subject, "", settings.EMAIL_FROM, [email], html_message=html_message)