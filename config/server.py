# -*- coding: utf8 -*-
# Django settings for iDentalk project.

# import os
# import sys 


# #自定义app加载路径
# PROJECT_ROOT = '/var/www/iDentalk/apps'
# sys.path.insert(0, os.path.join(PROJECT_ROOT, 'dentist_apps'))
# sys.path.insert(0, os.path.join(PROJECT_ROOT, 'patient_apps'))
# sys.path.insert(0, os.path.join(PROJECT_ROOT, 'public_apps'))
# sys.path.insert(0, os.path.join(PROJECT_ROOT, 'extra_apps'))
# sys.path.append('/var/www/iDentalk')


#
DATABASES = {
    'default': {
        'ENGINE': 'mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'iDentalk',                      # Or path to database file if using sqlite3.
        'USER': 'dbadmin',                      # Not used with sqlite3.
        'PASSWORD': '5$perDBinst',
        'HOST': 'identalkdb.co6kezkdcruj.us-east-1.rds.amazonaws.com',                      # Set to empty string for localhost. Not used with sqlite3.
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
TIME_ZONE = ''#America/New_York

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/var/www/iDentalk/uploaded/'  ##用户所上传的文件存放的根目录

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/var/www/iDentalk/templates",
    "/var/www/iDentalk/static/js/tmpl",
    "/var/www/iDentalk/static/mobile-app/tmpl",
)

STATIC_PATH='/var/www/iDentalk/static'   #静态文件的物理路径
STATIC_URL='/site_static/' #静态文件的URL前缀

