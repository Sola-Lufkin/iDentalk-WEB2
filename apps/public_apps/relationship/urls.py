# -*- coding: utf8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('relationship.views',

                        #Follow
                        url(r'^ajax/relationship/follow/(?P<object_id>\d+)$',
                            'follow',
                            name="follow"),
                        url(r'^ajax/relationship/unfollow/(?P<object_id>\d+)$',
                            'unfollow',
                            name="unfollow"),
        
                        #Connect
                        url(r'^ajax/relationship/connect/(?P<object_id>\d+)$',
                            'connect',
                            name="connect"),

                        url(r'^ajax/relationship/cancelrequest/(?P<object_id>\d+)$',
                            'connecting_cancel',
                            name="connecting_cancel"),

                        url(r'^ajax/relationship/unconnect/(?P<object_id>\d+)$',
                            'unconnect',
                            name="unconnect"),

                        url(r'^ajax/relationship/acceptrequest/(?P<object_id>\d+)$',
                            'accept_request',
                            name="check_con_yes"),

                        url(r'^ajax/relationship/refuserequest/(?P<object_id>\d+)$',
                            'refuse_request',
                            name="check_con_no"),
)