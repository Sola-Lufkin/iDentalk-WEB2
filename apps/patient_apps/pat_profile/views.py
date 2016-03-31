# -*- coding: utf8 -*-

import decimal, datetime
#
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User   
from django.utils.translation import ugettext_lazy as _ 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils import simplejson as json
#
from profile.forms import *
from profile.models import *
from public.views import _show_name, _show_obj_name, _count_age, to_homepage
from iDentalk import settings
from annoying.decorators import render_to, ajax_request
from utils import JsonResponse, json_serialize


def _get_pat_info_(request,object_id = ""):
    '''
    该函数获取病人的个人信息，并包装成包

    **参数**
    ``object_id``
        object_id默认或空字符串，代表所要获取的医生信息即为此时登录的医生的信息；
        object_id传入数字型的字符串，代表所要获取医生信息的id
    '''

    template_var = {}
    DATE_FORMAT = "%m-%d-%Y"
    myname = ""
    objname = ""
    title_var = ""
    if object_id == "":
        #myname = _show_name(request)       
        UserObj = User.objects.get(username=request.user)
        BaseObj = Base.objects.get(user=request.user)
        PatientProfileObj = PatientProfile.objects.get(user=request.user)

    else :
        #objname = _show_obj_name(object_id) 
        UserObj = User.objects.get(id=object_id)
        BaseObj = Base.objects.get(user=UserObj)
        PatientProfileObj = PatientProfile.objects.get(user=UserObj) 

        
    try:
        A = PatientProfileObj.medical_history.split(',')
        B = PatientProfileObj.treatment_history.split(',')
        C = PatientProfileObj.oral_habit.split(',')
        D = PatientProfileObj.oral_status.split(',')     
        
    except:
        A = ""
        B = ""
        C = ""
        D = ""
    own=False
    if UserObj == request.user:
        own=True
    title = PatientProfileObj.title
    
    if title == "1":
        title_var = "Mr."
    elif title == "2":
        title_var = "Miss."
    elif title == "3":
        title_var = "Ms."
    elif title == "4":
        title_var = "Mrs."

    latitude = str(PatientProfileObj.latitude)
    longitude = str(PatientProfileObj.longitude)
    latlng = "("+latitude+", "+longitude+")"

    try:
        Info = {
                "username":UserObj.username,
                "first_name":UserObj.first_name,
                "last_name":UserObj.last_name,
                "title":PatientProfileObj.title,
                #"middle_name":BaseObj.middle_name,
                #"show_mid_name":BaseObj.show_mid_name,
                "imagephoto":BaseObj.imagephoto.url,
                "imagebig":BaseObj.imagebig.url,
                "imagesmall":BaseObj.imagesmall.url,
                "summary":BaseObj.summary,
                "workemail":BaseObj.workemail,
                "gender":BaseObj.gender,
                "location":PatientProfileObj.location,
                "latlng":latlng,
                "birthday":BaseObj.birthday.strftime(DATE_FORMAT),
               }
    except:
        Info = {
                "username":UserObj.username,
                "first_name":UserObj.first_name,
                "last_name":UserObj.last_name,
                "title":PatientProfileObj.title,
                #"middle_name":BaseObj.middle_name,
                #"show_mid_name":BaseObj.show_mid_name,
                "imagephoto":BaseObj.imagephoto.url,
                "imagebig":BaseObj.imagebig.url,
                "imagesmall":BaseObj.imagesmall.url,
                "summary":BaseObj.summary,
                "workemail":BaseObj.workemail,
                "gender":BaseObj.gender,
                "location":PatientProfileObj.location,
                "latlng":latlng,
                # "birthday":BaseObj.birthday.strftime(DATE_FORMAT),
               }
    
    print Info["latlng"]
    template_var = {
                    'Info':Info,
                    'title_var':title_var,
                    'myname':UserObj.first_name +" "+ UserObj.last_name,
                    #'objname':objname,
                    'own':own,
                    'object_id':object_id,
                    'age':_count_age(request),
                    "A":A,
                    "B":B,
                    "C":C,
                    "D":D,
                 }

    return template_var



#病人的Profile页显示
@render_to("patient/patient_profile.html")
def pa_pro(request):
    ''''''
    template_var=_get_pat_info_(request)
    return template_var


@login_required
@csrf_exempt
@require_http_methods(['POST'])
def pat_pro_base(request):
    '''病人的基本信息填写 数据存储接口'''

    result = { "msg":"failure", "status":0 }           
    data = json.loads(request.POST["data"])
    '''
    前端使用Ajax遍历，show_mid_name未选中时，
    并不会传值过来，需要后端使用try方法手动赋值
    '''
    # try:
    #     show_mid_name = data["show_mid_name"]
    # except:
    #     show_mid_name = False

    try:
        User.objects.filter(username=request.user).update(
                                                       first_name=data["first_name"].strip(), 
                                                       last_name=data["last_name"].strip(),
                                                       )
        ## if user do not fill the birthday, it will failure. so we use "try"
        try:
            if data['title'] == '2' or data['title'] == '3' or data['title'] == '4':
                gender = 'F'
            if data['title'] == '1':
                gender = 'M'

            birthday = datetime.datetime.strptime(data["birthday"], '%m-%d-%Y')
            Base.objects.filter(user=request.user).update(
                                                          # middle_name=data["middle_name"], 
                                                          # show_mid_name=show_mid_name,
                                                          #workemail=data["workemail"],
                                                          birthday = birthday,
                                                          # gender=data["gender"],
                                                          gender=gender,
                                                          summary=data["summary"].strip(),
                                                        )

            # if data['title'] == 2 or data['title'] == 3 or data['title'] == 4:
            #     gender = 'F'
            # elif data['title'] == 1:
            #     gender = 'M'

            PatientProfile.objects.filter(user=request.user).update(title=data["title"])

        except:
            if data['title'] == '2' or data['title'] == '3' or data['title'] == '4':
                gender = 'F'
            if data['title'] == '1':
                gender = 'M'

            Base.objects.filter(user=request.user).update(
                                                          # middle_name=data["middle_name"], 
                                                          # show_mid_name=show_mid_name,
                                                          #workemail=data["workemail"],
                                                          # gender=data["gender"],
                                                          gender=gender,
                                                          summary=data["summary"].strip(),
                                                        )

            PatientProfile.objects.filter(user=request.user).update(title=data["title"])

        result = {"msg":"Success", "status":1}

    except:
        result = {"msg":"Failure", "status":0}

    return JsonResponse(result)


@login_required
@csrf_exempt
@require_http_methods(['POST'])
def pat_pro_pathology(request):

    result = { "msg":"Failure", "status":0 }       
    data = json.loads(request.POST["data"])
    print(data)  
    PatientProfile.objects.filter(user=request.user).update(
                                                            medical_history=data["dental_problem"],
                                                            treatment_history=data["dental_treatment"],
                                                            oral_habit=data["oral_habits"],
                                                            oral_status=data["oral_status"],
                                                            )
    result = {"msg":"Success", "status":1}
    return JsonResponse(result)


@login_required
@csrf_exempt
@require_http_methods(['POST'])
def pat_loc_edit(request):
    """ """

    # try:           
    if request.POST["latlng"] == '':
        latitude = longitude = 0
    else:
        latlng = request.POST["latlng"].replace("(",'').replace(")",'').split(', ') 
        latitude = decimal.Decimal(latlng[0])
        longitude = decimal.Decimal(latlng[1])
    location = request.POST["location"]
    location = location.strip()
    PatientProfile.objects.filter(user=request.user).update(location=location,
                                                            latitude=latitude,
                                                            longitude=longitude,
                                                            )
    result = {"msg":"Success", "status":1}

    # except:
        # result = {"msg":"failure", "status":0}
        
    return JsonResponse(result)