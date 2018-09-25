import re

from django_redis import get_redis_connection
from rest_framework import serializers

from QQ.models import AuthModel
from QQ.utils import OAuthQQ
from users.models import User


class BindUserSerializer(serializers.ModelSerializer):
    """用户序列化器"""

    # 添加模型所没有的序列
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    token = serializers.CharField(label='token', read_only=True)
    openid_token = serializers.CharField(label='绑定操作凭证', write_only=True)
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$', write_only=True)

    class Meta:
        # 绑定的模型
        model = User
        # 需要序列化/反序列化哪些字段
        fields = ('id', 'username', 'password', 'mobile', 'sms_code', 'openid_token', 'token')
        # 对所有序列做的补充
        extra_kwargs = {
            'username': {
                'read_only': True,
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate(self, attrs):

        # openid_token是否有效
        openid_token = attrs['openid_token']
        QQ = OAuthQQ()
        openid = QQ.check_save_user_token(openid_token)
        if openid is None:
            raise serializers.ValidationError('无效的openid_token')
        attrs['openid'] = openid

        # 手机号是否注册
        try:
            user = User.objects.get(mobile=attrs['mobile'])
        except User.DoesNotExist:
            raise serializers.ValidationError('手机号未注册')

        # 密码是否正确
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError('密码错误')
        else:
            attrs['user'] = user

        # 短信验证码是否正确
        mobile = attrs['mobile']
        redis_conn = get_redis_connection('verify_codes')
        sms_code = redis_conn.get('sms_%s' % mobile)
        sms_code = sms_code.decode() if sms_code else None
        if sms_code != attrs['sms_code']:
            raise serializers.ValidationError('短信验证码不正确')
        return attrs

    def create(self, validated_data):
        """上面的attrs是什么数据,validated_data就是什么数据"""

        # 必须获得用户,才可以绑定QQ
        user = validated_data['user']
        openid = validated_data['openid']
        AuthModel.objects.create(user=user, openid=openid)

        # 由服务器生成一个jwt-token数据,包含登录用户身份信息(以下五行->drf-jwt官方文档)
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        # 给user对象增加属性token,保存服务器生成的jwt-token数据
        user.token = token

        # 返回用户
        return user
