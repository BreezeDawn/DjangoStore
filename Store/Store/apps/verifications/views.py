# Create your views here.
import logging
import random

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection

from Store.libs.yuntongxun.sms import CCP
from celery_tasks.sms.tasks import send_sms_code
from verifications.contants import SMS_CODE_REDIS_EXPIRES, SMS_CODE_REDIS_TIMES, SMS_CODE_TEMP_ID

# 获取日志器
logger = logging.getLogger("django")


class VerificationsTest(APIView):
    """测试接口"""

    def get(self, request):
        return Response({"api": 'verificationstest'}, status=status.HTTP_200_OK)


class SMSCodeView(APIView):
    """获取短信验证码:
    1.1随机生成6位数字
    1.2在redis保存短信验证码内容,key=mobile,value=短信验证码
    1.3使用第三方平台发送短信
    """

    def get(self, request, mobile):
        # 建立redis连接,参数为配置文件缓存配置
        redis_conn = get_redis_connection('verify_codes')
        # 检测60s内是否已发送过
        time = redis_conn.get('sms_flag_%s' % mobile)
        if time:
            return Response({'message': '发送短信过于频繁'}, status=status.HTTP_400_BAD_REQUEST)

        # 1.1随机生成6位数字
        sms_code = "%06d" % random.randint(0, 999999)

        # 1.2在redis保存短信验证码内容,并设置短信验证码频繁发送时间
        # -- key = mobile, value = 短信验证码
        pl = redis_conn.pipeline()
        pl.setex('sms_%s' % mobile, SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('sms_flag_%s' % mobile, SMS_CODE_REDIS_TIMES, 1)
        pl.execute()

        # 短信验证码过期时间
        expires = SMS_CODE_REDIS_EXPIRES // 60

        # 1.3使用第三7方平台发送短信
        send_sms_code.delay(mobile,sms_code,expires)

        logger.info("短信验证码:%s" % sms_code)
        return Response({"message": "短信发送成功"}, status=status.HTTP_200_OK)
