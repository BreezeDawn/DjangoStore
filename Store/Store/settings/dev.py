"""
Django settings for Store project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 将sys.path中添加apps路径,以便寻找子应用
import sys

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8vc0jpqnif6b7rere*2v+c#sj$00+x1w3m3#j8mw5foq(sbc&0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 允许访问的host
ALLOWED_HOSTS = ['127.0.0.1','www.xingtu.info']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'QQ.apps.QqConfig',
    'verifications.apps.VerificationsConfig',
    'rest_framework',
    'corsheaders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

# 如果修改目录名,该配置需要被修改
ROOT_URLCONF = 'Store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 如果修改目录名,该配置需要被修改
WSGI_APPLICATION = 'Store.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'xiaodianchi',
        'NAME': 'Store'
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# 修改语言
LANGUAGE_CODE = 'zh-hans'
# 修改时区
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


# 设置缓存存入redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.default.DefaultClient"
        }
    },
    # 存放session
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.default.DefaultClient"
        }
    },
    # 存放短信验证码
    "verify_codes": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.default.DefaultClient"
        }
    },
}


# 设置session用缓存保存,而上面设置缓存用redis保存,所以session的缓存保存在了redis中
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# 使用名为'session'的redis配置
SESSION_CACHE_ALIAS = "session"


LOGGING = {
    # 保留字段
    'version': 1,

    # 是否禁用已经存在的日志器
    'disable_existing_loggers': False,

    # 日志信息显示的格式
    'formatters': {
        # 标准版
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s]'
                      '[%(filename)s:%(lineno)d][%(levelname)s][%(message)s]'
        },
        # 冗长版
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        # 简单版
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },

    # 对日志进行过滤
    'filters': {
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    # 日志流的处理方法
    'handlers': {

        # 把日志打印到终端
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },

        # 向文件中输出日志
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/store.log"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },

    },


    # 日志器
    'loggers': {
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    },

}


REST_FRAMEWORK = {
    # 异常处理
    'EXCEPTION_HANDLER': 'Store.utils.exceptions.drf_exception_handler',
    # 设置认证方案
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # JWT认证:json_web_token认证
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # Session:session_id认证
        'rest_framework.authentication.SessionAuthentication',
        # Basic:账号密码验证
        'rest_framework.authentication.BasicAuthentication',
    ),
}


# 指明用户模型
AUTH_USER_MODEL = 'users.User'


# CORS跨域请求(只针对异步请求如ajax)
# CORS白名单
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8080',
    'www.xingtu.info:8080',
)
# CORS允许携带cookie访问
CORS_ALLOW_CREDENTIALS = True


# JWT扩展设置
JWT_AUTH = {
    # 设置生成jwt-token数据时,token数据的有效时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 修改JWT登录视图返回值调用的函数,自定义相应函数
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'users.utils.jwt_response_payload_handler',
}

AUTHENTICATION_BACKENDS = [
        "users.utils.UsernameMobileModelBackend",
]

# QQ登录开发设置
QQ_CLIENT_ID = '101507886'  # APP ID
QQ_CLIENT_SECRET = '9c9915eb20bd631bdf11b528360cdc28'   # APP Key
QQ_REDIRECT_URI = 'http://www.xingtu.info:8080/qq-callback.html'  # 网站回调地址
QQ_STATE = '/'  # QQ成功登录之后跳转页面地址