# -*- coding: utf8 -*-
import os
# import sys

DATABASES = {
    'default': {
        'ENGINE': 'mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'iDentalk',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = 'uploaded/'  ##用户所上传的文件存放的根目录
# MEDIA_ROOT = 'http://img.identalk.com/' 

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath("templates"),
    os.path.abspath("static/js/tmpl"),
    os.path.abspath("static/mobile-app/tmpl"),
)

STATIC_PATH='./static'   #静态文件的物理路径
STATIC_URL='/site_static/' #静态文件的URL前缀

# STATIC_PATH='http://img.identalk.com/'   #静态文件的物理路径
# STATIC_URL='/site_static/' #静态文件的URL前缀
