# -*- coding: utf8 -*-
from django.conf.urls.defaults import *
# from django.views.generic.simple import direct_to_template

urlpatterns = patterns('notification.views',
                        #  Event

                        url(r'^notifications$',
                            'notice_get',
                            name="notice"),
                        
                        url(r'^ajax/listener/$',
                            'remind_count',
                            name='remind_count'),

                        url(r'^ajax/notifications/mark-read$', 
                            'notice_click',
                            name='notice_click'),

                        url(r'^ajax/requestnotice/archive/(?P<object_id>\d+)$',
                            'notice_archive'),

                        url(r'^ajax/mydentalk/mark-read$', 
                            'click_msg_notice',
                            name='click_msg_notice'), 
                        
                        # url(r'^dentist/msg/notifications$',
                        #     'msg_event',
                        #     name="msg_event"),

                        # url(r'^patient/msg/notifications$',
                        #     'msg_event',
                        #     name="msg_event2"),

)