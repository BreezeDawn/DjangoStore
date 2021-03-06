from celery import Celery

import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'Store.settings.dev'

import django
django.setup()

# 创建celery对象,名字随便起
celery_app = Celery("celery")

# 加载配置,路径以.分隔
celery_app.config_from_object("celery_tasks.config")

# 启动worker自动发现任务,路径以.分隔,自动寻找目录下的tasks文件中的装饰器对象
celery_app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email',])

