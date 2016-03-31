# -*- coding: utf8 -*-
# Django settings for iDentalk project.

import os
import sys

# import djcelery

# djcelery.setup_loader()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

#自定义app加载路径
PROJECT_ROOT = BASE_DIR + '/apps'
CONFIG_ROOT = BASE_DIR + '/config'

sys.path.insert(0, CONFIG_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'dentist_apps'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'patient_apps'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'public_apps'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'extra_apps'))


#diff config
DEBUG = True #False
from local import *
# from server import *

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# MEDIA_URL = '/webhost_media/'   ##media served 所使用的URL路径
MEDIA_URL = 'http://img.identalk.com/' ###

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'  ##admin后台所需的静态文件所对应的URL前缀

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'k121s+e#2w!e0e+=r3ptre)%a+)pt)q@c)zy_-w0a&y99v1&@l'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    #mobile detect
    'django_mobile.loader.Loader',

    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    #mobile detect
    'django_mobile.context_processors.flavour',
    'django.contrib.auth.context_processors.auth',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware', # for gzip Compression
    'django.middleware.http.ConditionalGetMiddleware', # for etag & last-modify date info

    #mobiel detect
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
)

ROOT_URLCONF = 'iDentalk.urls'

#S3
S3_ACCESS_KEY='AKIAIGXMYRB2RYHPTK2Q'
S3_SECRET_KEY='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'
S3_BUCKET='img.identalk.com'


#登录后跳转至
# LOGIN_REDIRECT_URL = '/dentist/profile'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    #Extra Apps 
    'annoying',
    'south',
    'registration',
    'captcha',
    #'sorl.thumbnail',
    # mobile detect
    'django_mobile',
    
    #Own Apps
    'imgupload',
    'profile',
    'accounts',
    'relationship',
    'dentist',
    'patient',
    'gallery',
    'stream',
    'notification',
    'public',
    'den_profile',
    'pat_profile',
    'den_manage',
    'iDenMail',
    'search',
)

# INSTALLED_APPS += ('djcelery', )

# CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

# 配置邮箱的文件
# EMAIL_HOST = 'smtp.exmail.qq.com'
# EMAIL_PORT = '25'
# EMAIL_HOST_USER = 'noreply@identalk.com'
# EMAIL_HOST_PASSWORD = '5$/talk'
# EMAIL_USE_TLS = True

EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'AKIAICZ224TPW3R4NTVA'
EMAIL_HOST_PASSWORD = 'Al8AMHgLsXUv/tn2S+Q8WcUwRNQhnGM4dAouuokqi0lp'
EMAIL_USE_TLS = True
SERVER_EMAIL = 'noreply@identalk.com'
DEFAULT_FROM_EMAIL = 'noreply@identalk.com'
TO_EMAIL = 'r@identalk.com'

ACCOUNT_ACTIVATION_DAYS = 2 #激活时间




# BROKER_URL = 'redis://localhost:6379/0'
