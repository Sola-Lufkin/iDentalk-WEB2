# -*- coding: utf8 -*-
from django.conf.urls.defaults import *
# from django.views.generic.simple import direct_to_template

urlpatterns = patterns('accounts.views',

                        url(r'^login/$',
                            'loginfunction',        
                            ),
                        # url(r'^logout/$',
                        #     'logout',
                        #     )
						# 登录
						url(r'^login/$',
							'login',
							{'template_name':'index.html'},name="login"
							),
                        url(r'^apply/$',
                            'apply',
                            name='apply'),
                        # url(r'^signup/$',
                        #     'idchoose',
                        #     name="idchoose"),
                        url(r'^signup/d$',
                            'd_signup',{'backend': 'registration.backends.default.DefaultBackend'},
                            name="d_signup"),

                        url(r'^signup/p$',
                            'p_signup',{'backend': 'registration.backends.default.DefaultBackend'},
                            name="p_signup"),

                        # oauth & func
                        url(r'^oauth$',
                            'goo_oauth_invite_friends',
                            name='goo_oauth_invite_friends'),

                        url(r'^invite_contacts/$',
                            'invite_contacts',
                            name="invite_contacts"
                            ),

                        url(r'^invite_friends$',
                            'manual_invite_friends',
                            name='manual_invite_friends'),

                        url(r'^fb/oauth$',
                            'fb_oauth_post_wall',
                            name='fb_oauth_post_wall'),

                        url(r'^ms/oauth$',
                            'ms_oauth_invite_friends',
                            name='ms_oauth_invite_friends'),
)