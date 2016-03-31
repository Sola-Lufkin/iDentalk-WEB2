# -*- coding: utf8 -*-
from django.conf.urls.defaults import *
# from django.views.generic.simple import direct_to_template
from django.contrib import admin
import settings
admin.autodiscover()


urlpatterns = patterns('',

                      url(r'^admin/', 
                         include(admin.site.urls)),
                      url(r'^accounts/', 
                          include('registration.urls')),
                      url(r'^captcha/', 
                          include('captcha.urls')),
                      url(r'',
                          include('accounts.urls')),
                      url(r'',
                          include('public.urls')),
                      url(r'',
                          include('profile.urls')),
                      url(r'',
                          include('dentist.urls')),
                      url(r'',
                          include('den_profile.urls')),
                      url(r'',
                          include('patient.urls')),
                      url(r'',
                          include('pat_profile.urls')),
                      url(r'',
                          include('gallery.urls')),
                      url(r'',
                          include('stream.urls')),
                      url(r'',
                          include('notification.urls')),
                      url(r'',
                          include('relationship.urls')),
                      url(r'',
                          include('iDenMail.urls')),
                      url(r'',
                          include('search.urls')),
    
                      #设置静态文件在服务器端的存储地址
                      url(r'^site_static/(?P<path>.*)$',
                          'django.views.static.serve',
                          {'document_root': settings.STATIC_PATH}),
        
                      #设置上传后的图片文件物理路径所对应的url路径
                      url(r'^webhost_media/(?P<path>.*)$',
                          'django.views.static.serve',
                          {'document_root': settings.MEDIA_ROOT}),   

)