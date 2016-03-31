# -*- coding: utf8 -*-
from django.conf.urls.defaults import *
# from django.views.generic.simple import direct_to_template

urlpatterns = patterns('gallery.views',

                        #医生病例模块
                        url(r'^ajax/d/gallery/getcases/$',
                            'case_list',
                            name="case_list"),

                        url(r'^ajax/d/(?P<uid>\d+)/gallery/getcases/$',
                            'case_list',
                            name="case_list"),

                        url(r'^gallery/(?P<uid>\d+)/case/$',
                            'case_list_big',
                            name="case_list_big"),

                        url(r'^gallery/(?P<uid>\d+)/case/(?P<case_id>\d+)$',
                            'case_detail',
                            name="case_detail"),

                        ##
                        # url(r'^dentist/case/detail/(?P<object_id>\d+)$',
                        #     'case_detail',
                        #     name="case_detail"),
                        
                        # url(r'^dentist/(?P<user_id>\d+)/case/detail/(?P<object_id>\d+)$',
                        #     'case_detail_view',
                        #     name="case_detail_view"),
                        ##

                        url(r'^ajax/gallery/case/addbase/$',
                              'case_base_add',
                              name='case_base_add'),

                        url(r'^ajax/gallery/case/addimg/$',
                              'case_img_add',
                              name='case_img_add'),

                        url(r'^ajax/gallery/case/updatebase/$', 
                            'case_info_update', 
                            name="case_info_update"),

                        # url(r'^dentist/case/desc_update$', 
                        #     'case_desc_update', 
                        #     name="case_desc_update"),

                        url(r'^ajax/gallery/case/delete/$', 
                            'case_delete',
                            name="case_delete"),

                        url(r'^ajax/gallery/case/deleteimg/$', 
                            'case_img_delete',
                            name="case_img_delete"),
                        
)