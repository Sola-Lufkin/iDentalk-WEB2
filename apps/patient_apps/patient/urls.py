# -*- coding: utf8 -*-
from django.conf.urls.defaults import *
# from django.views.generic.simple import direct_to_template

urlpatterns = patterns('patient.views',

                        url(r'^p/home/[\S]{0,36}',
                            'pat_homepage',
                            name="pat_homepage"),

                        # mobile version 医生列表页面
                        url(r'^p/dlist/$',
                            'den_list',
                            name='den_list'
                            ),

                        url(r'^p/(?P<pid>\d+)$',
                            'pat_pathology',
                            name="pat_pathology"),

                        url(r'^patient/profile$',
                            'pat_dental_record',
                            name="dental_record"),

                        # calendar
                        url(r'^p/(?P<pid>\d+)/calendar/$',
                            'calendar',
                            name='calendar'),

                        url(r'^p/getcalendar/$',
                            'get_calendar',
                            name='get_calendar'),

                        url(r'^p/putcalendar/$',
                            'put_calendar',
                            name='put_calendar'),

                        url(r'^p/updatecalendar/$',
                            'update_calendar',
                            name='update_calendar'),
 
                        url(r'^p/deletecalendar/$',
                            'delete_calendar',
                            name='delete_calendar'),

)