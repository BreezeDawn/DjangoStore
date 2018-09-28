from django.db import models
from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer, BadData
from django.conf import settings
# Create your models here.
from Store.utils.models import BaseModel
from users.constants import VERIFY_EMAIL_TOKEN_EXPIRES


class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name='默认地址')
    ...

    class Meta:
        db_table = 'st_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def verify_email_url(self):
        """生成对应用户的邮箱验证地址"""
        # 组织用户数据
        data = {
            'id': self.id,
            'email': self.email
        }
        # 进行加密
        serializer = TimedJSONWebSignatureSerializer(secret_key=settings.SECRET_KEY,
                                                     expires_in=VERIFY_EMAIL_TOKEN_EXPIRES)
        token = serializer.dumps(data).decode()
        # 拼接验证链接地址
        verify_url = 'http://www.xingtu.info:8080/success_verify_email.html?token=%s' % token
        return verify_url

    @staticmethod
    def check_verify_email(token):
        """校验用户邮箱地址"""

        # 解密token
        serializer = TimedJSONWebSignatureSerializer(secret_key=settings.SECRET_KEY,
                                                     expires_in=VERIFY_EMAIL_TOKEN_EXPIRES)
        try:
            data = serializer.loads(token)
        except BadData:
            return None

        # 根据解密数据查询用户
        email = data.get('email')
        user_id = data.get('id')
        try:
            user = User.objects.get(id=user_id, email=email)
        except User.DoesNotExist:
            return None
        else:
            return user


class Address(BaseModel):
    """
    用户地址
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses',
                                 verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses',
                                 verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
