# -*- coding: utf8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('search.views',

                        # url(r'^search_newnew$',
                        #     'search_newnew'
                        #     ),

                        url(r'^name-search/[\S]{0,36}$',
                            'search_by_name',
                            name="search_by_name"
                            ),

                        # serve for top navigation search form.
                        url(r'^ajax/name-search-nav/(?P<keyword>.*)$',
                            'search_by_name',
                            name="search_by_name"
                            ),

                        #add by fu for geoloc search
                        url(r'^geoloc-search/myloc/$',
                            'search_geoloc_range_fixed_loc',
                            name="search_by_myloc"
                            ),

                        url(r'^geoloc-search/otherloc/$',
                            'search_geoloc_range_free_loc',
                            name="search_by_other"
                            ),

                        url(r'^ajax/geoloc-range/$',
                            'search_geoloc_range',
                            name="geoloc_range"
                            ),
)