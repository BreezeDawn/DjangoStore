# 封装队列任务函数
from celery_tasks.main import celery_app
from celery_tasks.sms.yuntongxun.sms import CCP
import logging

logger = logging.getLogger('django')

SMS_CODE_TEMP_ID = 1

@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code, expires):
    print('[celery]第三方发送短信开始 --> [mobile: %s]-[验证码: %s]' % (mobile, sms_code))
    try:
        res_code = CCP().send_template_sms(mobile, [sms_code, expires], SMS_CODE_TEMP_ID)
    except BaseException as e:
        logger.error('[celery]第三方发送短信异常 --> [mobile: %s]-[验证码: %s]' % (mobile, sms_code))
    else:
        if res_code:
            logger.error('[celery]第三方发送短信失败 --> [mobile: %s]-[验证码: %s]' % (mobile, sms_code))
        else:
            logger.info('[celery]第三方发送短信成功 --> [mobile: %s]-[验证码: %s]' % (mobile, sms_code))


