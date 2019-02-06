from local_settings import *

ROOT_URLCONF = 'server.urls'
INSTALLED_APPS = [
    'server.apps.ServerConfig',
]
MIDDLEWARE = [
]

EMAIL_SUBJECT_PREFIX = ''
ADMINS = [('Admin', 'i@0x01.me')]
DEFAULT_FROM_EMAIL = 'no-reply@0x01.me'
SERVER_EMAIL = 'share.api@0x01.me'

USE_I18N = False
USE_L10N = False
USE_TZ = False
TIME_ZONE = 'Asia/Shanghai'
