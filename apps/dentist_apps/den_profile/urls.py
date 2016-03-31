# -*- coding: utf8 -*-
from django.conf.urls.defaults import *
# from django.views.generic.simple import direct_to_template

urlpatterns = patterns('den_profile.views',

                        url(r'^ajax/d/profile/$',
                            'den_pro',
                            name="den_pro"),

                        #公共角度医生Profile页
                        url(r'^ajax/d/(?P<object_id>\d+)/profile/$',
                            'den_pro',
                            name="den_pro_view"),                                 

                        url(r'^ajax/d/profile/editbase/$',
                            'den_pro_base',
                            name="den_pro_base"),

                        url(r'^d/profile/addprovepic/$',
                            'add_prove_pic',
                            name="add_prove_pic"),  

                        url(r'^ajax/d/profile/addclinic/$',
                            'den_pro_loc_add',
                            name="den_pro_loc_add"),

                        url(r'^ajax/d/profile/editclinic/(?P<object_id>\d+)$',
                            'den_pro_loc_edit',
                            name="den_pro_loc_edit"),

                        url(r'^ajax/d/profile/deleteclinic/(?P<object_id>\d+)$',
                            'den_pro_loc_delete',
                            name="den_pro_loc_delete"), 

                        url(r'^ajax/d/profile/editfield/$',
                            'den_pro_Tag_edit',
                            {'tagtype':'F'},
                            name="den_pro_Tag_edit"),

                        url(r'^ajax/d/profile/editdegree/$',
                            'den_pro_Tag_edit',
                            {'tagtype':'D'},
                            name="den_pro_Deg_edit"),
)