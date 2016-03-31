# -*- coding: utf8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('dentist.views',

                        #医生主页
                        url(r'^d/(?P<object_id>\d+)/[\S]{0,100}$',
                            'den_homepage',
                            name="den_homepage_view"),

                        # url(r'^dentist/(?P<object_id>\d+)/[\S]{0,36}$',
                        #     'den_homepage',
                        #     name="den_homepage_view"),

                        url(r'^d/home/[\S]{0,100}$',
                            'den_homepage',
                            name="den_homepage"),

                        # qa
                        url(r'^ajax/d/(?P<uid>\d+)/qa/getqa/$',
                            'get_qa',
                            name='get_qa'),

                        url(r'^ajax/d/putqa/$',
                            'put_qa',
                            name='put_qa'),

                        url(r'^ajax/d/updateqa/$',
                            'update_qa',
                            name='update_qa'),

                         url(r'^ajax/d/moveqaplace/$',
                            'move_qa_place',
                            name='move_qa_place'),

                        url(r'^ajax/d/deleteqa/$',
                            'delete_qa',
                            name='delete_qa'),

                        
                        #医生的病人管理页面
                        url(r'^d/manage/$',
                            'pat_manage',
                            name="pat_manage"),

                        #病人列表 暂用于mobile version
                        url(r'^d/plist/$',
                            'pat_list',
                            name="pat_list"
                            ),
                        #拉取主页信息
                        # url(r'dentist/home$',
                        #     'get_den_homepage',
                        #     name="get_den_homepage"),

                        # url(r'dentist/(?P<object_id>\d+)/home$',
                        #     'get_den_homepage',
                        #     name="get_den_homepage"),

                        # url(r'^dentist/push$',
                        #     'den_homepage_pushed',
                        #     name="den_homepage_pushed"),
                        # url(r'^dentist/push_cancel$',
                        #     'den_homepage_pushed_cancel',
                        #     name="den_homepage_pushed_cancel"),

)