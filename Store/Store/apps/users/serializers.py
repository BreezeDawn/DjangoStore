import re

from django_redis import get_redis_connection
from rest_framework import serializers

from users.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """用户序列化器"""

    # 添加模型所没有的序列
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    allow = serializers.CharField(label='是否同意协议', write_only=True)
    token = serializers.CharField(label='jwt-token', read_only=True)

    class Meta:
        # 绑定的模型
        model = User
        # 需要序列化/反序列化哪些字段
        fields = ('id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow','token')
        # 对所有序列做的补充
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
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

    # 校验数据完整性 -> 序列化器不指定null都必须要传

    def validate_username(self, value):
        """用户名格式"""
        # 不以数字开头
        if re.match(r'^\D.*', value) is None:
            raise serializers.ValidationError('用户名请以非数字开头')
        return value

    def validate_mobile(self, value):
        """手机号格式/是否已被注册"""
        # 11位数字
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式不正确')

        # 是否被注册
        count = User.objects.filter(mobile=value).count()
        if count:
            raise serializers.ValidationError('手机号已被注册')
        return value

    def validate_allow(self, value):
        """是否同意协议"""
        if value != 'true':
            raise serializers.ValidationError('请同意协议')
        return value

    def validate(self, attrs):
        """多数据校验"""
        # 两次密码是否一致
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两次密码不一致')

        # 短信验证码是否正确
        mobile = attrs['mobile']
        redis_conn = get_redis_connection('verify_codes')
        sms_code = redis_conn.get('sms_%s' % mobile)
        sms_code = sms_code.decode() if sms_code else None
        if sms_code != attrs['sms_code']:
            raise serializers.ValidationError('短信验证码不正确')
        return attrs

    def create(self, validated_data):
        """创建用户"""

        # 删除生成用户不必要的信息
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        # 创建用户并生成用户对象
        user = User.objects.create_user(**validated_data)

        # 由服务器生成一个jwt-token数据,包含登录用户身份信息(以下五行->drf-jwt官方文档)
        from rest_framework_jwt.settings import api_settings

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # 生成载荷
        payload = jwt_payload_handler(user)
        # 生成jwt-token
        token = jwt_encode_handler(payload)

        # 给user对象增加属性token,保存服务器生成的jwt-token数据
        user.token = token

        # 返回注册用户
        return user
