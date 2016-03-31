# -*- coding: utf8 -*-
from django.conf.urls.defaults import *
# from django.views.generic.simple import direct_to_template

urlpatterns = patterns('pat_profile.views',
 

                        #病人profile填写
                        url(r'^p/profile/$',
                            'pa_pro',
                            name="pa_pro"),

                        # url(r'^patient/profile/edit$',
                        #     'pa_pro_edit',
                        #     name="pa_pro_edit"),

                        url(r'^ajax/p/profile/editbase/$',
                            'pat_pro_base',
                            name="pat_pro_base"),

                        url(r'^ajax/p/profile/questionnaire/',
                            'pat_pro_pathology',
                            name='pat_pro_pathology'),

                        url(r'^ajax/p/profile/editlocation/$',
                            'pat_loc_edit',
                            name="pat_loc_edit"),
                        
                        # url(r'^patient/profile/img$',
                        #     'pro_img',
                        #     name="pro_img"),
)