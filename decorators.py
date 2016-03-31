# -*- coding: utf8 -*-
try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.

from django.utils.decorators import decorator_from_middleware, available_attrs
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User   
#
from iDentalk import settings
from profile.models import Base



def require_identity_type(idtype):
    '''
    修饰器 require_identity_type 用于在函数执行前对函数进行身份要求的修饰，
    如果不满足身份要求，将跳转到ErrorPage

    **参数**
    ``idtype``
        参数idtype的值必须为字符串 "Dentist" 或者 "Patient"
    '''

    if idtype == "Dentist":
        identity = "D"
    elif idtype == "Patient":
        identity = "P"
    def decorator(func):
        def inner(request, *args, **kwargs):
            BaseObj = Base.objects.get(user = request.user)
            try:
                if BaseObj.identity != identity:
                    print("Identity isn't %s, let's jump to ErrorPage" %idtype)
                    #tup = login_url, redirect_field_name, path
                    #return HttpResponseRedirect('%s?%s=%s' % tup)
                    return HttpResponseRedirect('/error')
            except:
                print("idtype参数传入有误，必须为Dentist 或者 Patient") 
            return func(request, *args, **kwargs)
        return wraps(func, assigned=available_attrs(func))(inner)

    return decorator


def steps_wrapped(view_func):
    '''
    该函数仿照Djangon内部csrf_view_exempt写成,
    为steps_require_unfinished所调用
    '''

    def wrapped_view(request, *args, **kwargs):
        BaseObj = Base.objects.get(user = request.user)
        if BaseObj.finish_steps :
            print("已经完成了基本信息填写步骤，不能再进入该填写页面，自动跳转回到主页")
            return HttpResponseRedirect(reverse("to_homepage"))
        return view_func(request, *args, **kwargs)
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)


def steps_require_unfinished(view_func):
    '''
    该修饰器用于限制已经完成Steps的用户再次进入Steps页面
    '''

    return steps_wrapped(view_func) 




