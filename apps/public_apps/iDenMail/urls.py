# -*- coding: utf8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('iDenMail.views',

                        url(r'^ajax/mydentalk/sendmsg/$',
                            'post_mail',
                            name ='post_mail'
                            ),

                        # url(r'^contact_list$',
                        #     'contact_list',
                        #     name='contact_list'
                        #     ),

                        url(r'^mydentalk/(?P<object_id>\d+)$',
                            'mail_history',
                            name= 'mail_history'
                            ),

                        url(r'^mydentalk/$',
                            'mails',
                            name = 'mails'
                            ),

                        # url(r'main$',
                        #     'main',
                        #     ),

)