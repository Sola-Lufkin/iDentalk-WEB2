# -*- coding: utf8 -*-
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('profile.views',

        
                        #病人注册页面
                        url(r'^step-p/$',
                            'patientstep',
                            name = "patientstep"),

                        url(r'^ajax/step-p/info/$',
                            'fill_info_pat',
                            name="fill_info_pat"
                            ),
        
                        #医生注册页面
                        url(r'^step-d/$',
                            'dentiststep',
                            name = "dentiststep"),

                        url(r'^ajax/step-d/info/$',
                            'fill_info_den',
                            name="fill_info_den"
                            ),

                        #头像
                        url(r'^ajax/saveimg/$', 
                            'save_img',
                            name="choose_avatar"
                            ),

                        url(r'^ajax/cutimg/$', 
                            'make_avatar',
                            name="upload_avatar"
                            ),

                        #证明图    
                        url(r'^ajax/upload-proof/$', 
                            'upload_proof',
                            name="upload_proof"
                            ), 
                        
                        url(r'^step-finished/$', 
                            'change_to_finished',
                            name='change_to_finished'
                            ), 
                        

                        #错误页                        
                        url(r'^error$',
                            direct_to_template,{'template':'error.html'},
                            name="error"),

                        #settings
                        url(r'^account/settings/$',
                            'settingpage',
                            name='settings'),
)