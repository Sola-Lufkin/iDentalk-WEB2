# -*- coding: utf8 -*-
import uuid
from django.utils import simplejson as json
from django.http import HttpResponse
from django.core import serializers
from datetime import datetime, timedelta, tzinfo
import math

class JsonResponse(HttpResponse):
    def __init__(self, obj, **kw):
        super(JsonResponse, self).__init__(
            json.dumps(obj), mimetype='application/json', **kw)

def gen_guid():
    return unicode(uuid.uuid4()).replace('-', '')

def json_serialize( obj ):
	return serializers.serialize('json', obj)

def humantime(value):
    '''
    Time Transform for time delta between now and entry saved time in DB 
    to human readable time. such as, seconds ago, minutes ago, hours ago
    @version 0.1.2
    '''

    # print 'start'
    now = datetime.now()  # seconds from nowa time
    # print 1111
    ## now = timemodule.mktime(now) # from datetime time struct make seconds
    ## value = timemodule.mktime(value)
    ## delta = now - value  # seconds delta
    dt_delta = now - value  # seconds delta between noware time and past time value
    delta = dt_delta.total_seconds
    second_delta = dt_delta.seconds
    day_delta = dt_delta.days
    # print(u'comment datetime is : %s' % value)
    # print(u'now datetime is : %s' % now)

    # print(u'datetime delta is : %s' % dt_delta)
    # print(u'second_delta is : %s' % second_delta)
    # print(u'day_delta is : %s' % day_delta)

    if day_delta == 0:

        if second_delta == 0:
            return 'now'
        elif second_delta == 1:
            return '1 second ago'
        elif 1 < second_delta < 60:
            return u'%s seconds ago' % int(second_delta)
        elif 60 <= second_delta < 60*2:
            return u'1 minute ago'
        elif 60 < second_delta < 3600:
            return u'%s minutes ago' % int(math.floor(second_delta / 60))
        elif 3600 <= second_delta < 3600*2:
            return u'1 hour ago'
        elif 3600 < second_delta < 3600*24:
            return u'%s hours ago' % int(math.floor(second_delta / 3600))

    else:    # stands for dt_delta.days >= 1
        if day_delta == 1:
            return u'1 day ago'
        elif 1 < day_delta < 7:
            return u'%s days ago' % int(day_delta)
        elif 7 <= day_delta < 7*2:
            return u'1 week ago'
        elif 7*2 <= day_delta < 7*4:
            return u'%s weeks ago' % int(math.floor(day_delta / 7))
        elif 30 <= day_delta < 30*2:
            return u'1 month ago'
        elif 30*2 <= day_delta < 30*12:
            return u'%s months ago' % int(math.floor(day_delta / 30))
        elif 30*12 <= day_delta < 30*12*2:
            return u'1 year ago'
        elif 30*12*2 <= day_delta:
            return u'%s years ago' % int(math.floor(day_delta / 30*12))
