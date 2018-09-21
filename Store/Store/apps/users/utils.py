import re

from django.contrib.auth.backends import ModelBackend

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """自定义JWT自有登录视图返回值"""
    return {
        'user_id': user.id,
        'username': user.username,
        'token': token,
    }


class UsernameMobileModelBackend(ModelBackend):
    """自定义登录认证时校验数据(原本使用django自带ModelBackend)"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if re.match(r'1[3-9]\d{9}', username):
                # 根据手机号查询用户
                user = User.objects.get(mobile=username)
            else:
                # 根据用户名查询用户
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        else:
            # 如果存在user,校验用户的密码
            user.check_password(password)
        # 校验成功,返回user对象
        return user
