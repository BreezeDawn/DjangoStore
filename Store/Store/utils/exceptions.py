import logging

from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response

# 选择日志器,开启日志记录
logger = logging.getLogger('django')


def drf_exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 异常
    :param context: 抛出异常的上下文
    :return: Response响应对象
    """
    # 调用drf框架原生的异常处理方法
    response = exception_handler(exc, context)

    if response is None:
        # 取出异常上下文
        view = context['view']
        # 数据库异常
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            # 日志记录异常
            logger.error('[%s] %s' % (view, exc))
            # 自定义数据库异常的响应
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response
