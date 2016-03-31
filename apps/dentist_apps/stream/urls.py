# -*- coding: utf8 -*-
from django.conf.urls.defaults import *
# from django.views.generic.simple import direct_to_template

urlpatterns = patterns('stream.views',
                        
                        url(r'^ajax/d/stream/post/$',
                            'post_save',
                            name="post_save"),
                        
                        url(r'^ajax/d/stream/post_img/$',
                            'upload_post_img',
                            name="upload_post_img"),

                        url(r'^ajax/d/stream/getpost/$',
                            'post_get',
                            name='post_get'),

                        url(r'^ajax/d/(?P<object_id>\d+)/stream/getpost/$', # Public View on Dentist HomePage
                            'post_get',
                            name='public_post_get'),

                        url(r'^ajax/d/stream/deletepost/$',
                            'post_delete',
                            name="post_delete"),

                        url(r'^ajax/stream/comment/$',
                            'comment_save',
                            name='comment_save'),
                        
                        url(r'^ajax/d/stream/getcomment/$',
                            'comment_get',
                            name='comment_get'),
                        
                        url(r'^ajax/d/stream/deletecomment/$',
                            'comment_delete',
                            name="comment_delete"),

                        url(r'^ajax/p/stream/getpost/$',  # Patient start
                            'timeline_post_get',
                            name='timeline_post_get'),

                        url(r'^ajax/p/stream/getcomment/$',  # Patient start
                            'timeline_comment_get',
                            name='timeline_comment_get'),

                        url(r'^stream/getpost/(?P<object_id>\d+)$',
                            'notice_post_get',
                            name="notice_post_get")

)