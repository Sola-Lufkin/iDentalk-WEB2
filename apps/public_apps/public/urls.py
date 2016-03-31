# -*- coding: utf8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('public.views',

                        # 主页
                        # url(r'^index$','index', 
                        url(r'^$','index', 
                           {'backend': 'registration.backends.default.DefaultBackend'}),

                        #先转至HomePage
                        url(r'^to-homepage/$', 
                            'to_homepage',
                            name="to_homepage"),

                        url(r'^send-email/',
                        	'send_email',
                        	name="send_email"),

                        url(r'^sended-email/',
                            'email_sended',
                            name="email_sended"),
)
