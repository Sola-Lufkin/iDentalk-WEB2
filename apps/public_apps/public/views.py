# -*- coding: utf8 -*-
import os
import datetime
#
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site   
from django.utils.translation import ugettext_lazy as _   
#
from notification.models import Event
from profile.models import *
#from imgupload.views import *
from accounts.views import loginfunction
from iDentalk import settings
# from registration.views import register
from accounts.forms import LoginForm
from registration.forms import RegistrationForm
from registration.models import RegistrationProfile
from annoying.decorators import ajax_request
from utils import JsonResponse, json_serialize
from django.contrib.contenttypes.models import ContentType
from annoying.decorators import render_to, ajax_request



@csrf_exempt
@render_to("index.html")
def index(request, backend):
    '''
    Index主页
    '''

    template_var = {}
    form_login = LoginForm()
    loginfunction(request)
    template_var = {
                    "form_login":form_login,
                    }
    ##identity use for jumping to the right homepage when user click the "Home Page"
    try:
        template_var["identity"]=Base.objects.get(user=request.user).identity
        ##修复Bug#10 防止已经登录的用户再次进入index页面
        if template_var["identity"] == "D":
            return HttpResponseRedirect(reverse("to_homepage"))
        elif template_var["identity"] == "P":
            return HttpResponseRedirect(reverse("to_homepage"))
    except:
        pass
    return template_var


@login_required
def to_homepage(request):
    '''按身份跳转至对应HomePage跳转'''

    BaseObj = Base.objects.get(user=request.user)
    if BaseObj.identity == "D":
        
        return HttpResponseRedirect(reverse("den_homepage"))        
    else :
        
        return HttpResponseRedirect(reverse("pat_homepage"))     


def _show_obj_name(object_id):
    '''返回指定用户的姓名信息'''

    UserObj = User.objects.get(id=object_id)
    BaseObj = Base.objects.get(user=UserObj)
    objname = ""
    # if BaseObj.show_mid_name:
    #     objname = UserObj.first_name +" "+ BaseObj.middle_name +" "+ UserObj.last_name
    #     return objname
    # else:
    objname = UserObj.first_name +" "+ UserObj.last_name
    return objname


def _show_name(request):
    '''返回当前登录用户自己的姓名信息'''

    UserObj = User.objects.get(username=request.user)
    BaseObj = Base.objects.get(user=request.user)
    myname = ""
    
    # if BaseObj.show_mid_name:
    #     myname = UserObj.first_name +" "+ BaseObj.middle_name +" "+ UserObj.last_name
    #     return myname
    # else:
    myname = UserObj.first_name +" "+ UserObj.last_name
    return myname


def _count_age(request):
    '''根据生日计算年龄'''

    BaseObj = Base.objects.get(user=request.user)
    DATE_FORMAT = "%Y%m%d"
    age = ""
    try:
        X = int(datetime.datetime.now().strftime(DATE_FORMAT)) - int(BaseObj.birthday.strftime(DATE_FORMAT)) 
        Y = str(X)
        #通过相减值的位数长度判断用户年龄位数，从而取得相对应的值（即舍去后四位数）
        if len(Y) == 5:
            Z = Y[0]
        elif len(Y) == 6:
            Z = Y[0]+Y[1]       
        elif len(Y) == 7:
            Z = Y[0]+Y[1]+Y[2] 
        elif len(Y) < 4:
            Z = "0"
        age = int(Z) 
    except:
        pass
     
    return age 

def send_email(request):

    template_var = {}
    registration_profile = RegistrationProfile.objects.get(user=request.user)
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)

    registration_profile.send_activation_email(site)

    return HttpResponseRedirect(reverse("email_sended")) 

@render_to("registration/email_sended.html")
def email_sended(request):
    template_var={}
    return template_var