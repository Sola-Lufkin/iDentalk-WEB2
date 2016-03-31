    # -*- coding: utf8 -*-
import os
import random
import string
#import datetime
#
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User   
from django.utils.translation import ugettext_lazy as _ 
from django.contrib.auth.decorators import login_required
from forms import *
import Image
from Image import EXTENT
#
from profile.models import *
from imgupload.views import _imgupload, _imgcut, _uptoS3
from public.views import _show_name, _count_age, to_homepage
from iDentalk import settings
from iDentalk.decorators import require_identity_type, steps_require_unfinished

from annoying.decorators import render_to, ajax_request
from utils import JsonResponse, json_serialize
from django.utils import simplejson as json
from utils import gen_guid
import cStringIO


@require_identity_type("Patient")
@steps_require_unfinished
@csrf_exempt
@render_to("profile/patient_pro/patient_step.html")
def patientstep(request):
    '''
    病人Steps页面函数
    '''

    BaseObj = Base.objects.get(user=request.user)
    template_var={}
    form = PatientStep1() 
    template_var["form"]=form       
    return template_var

@csrf_exempt
@ajax_request
def fill_info_pat(request):
    '''
    Step中，病人填写姓名信息时所用的Ajax接口
    '''

    result={}
    if request.method == "POST":
        try:            
            data = json.loads(request.POST['data'])       
            first_name=data["first_name"].strip()
            last_name=data["last_name"].strip()
            title = data["title"]

            UserObj=User.objects.get(username=request.user)
            PatientProfileObj=PatientProfile.objects.get(user=request.user)
            UserObj.first_name=first_name 
            UserObj.last_name=last_name    
            UserObj.save()
            PatientProfileObj.title=title
            PatientProfileObj.save()

            result = {
                        "msg":"Success",
                        "status":"1",
            }
        except:
            result = {
                        "msg":"Failure",
                        "status":"0",
            }
           
    return result


@require_identity_type("Dentist")
@steps_require_unfinished
@csrf_exempt
@render_to("profile/dentist_pro/dentist_step.html")
def dentiststep(request):
    '''
    医生Steps页面函数
    '''

    BaseObj = Base.objects.get(user=request.user)
    template_var={}
    form = DentistStep1() 
    template_var["form"]=form       
    return template_var


@require_identity_type("Dentist")
@csrf_exempt
@ajax_request
def fill_info_den(request):
    '''
    Step中，医生填写姓名信息时所用的Ajax接口
    '''

    result = {}   
    if request.method=="POST":
        data = json.loads(request.POST['data'])
        first_name = data["first_name"].strip()
        last_name = data["last_name"].strip()
        title = data["title"]

        UserObj=User.objects.get(username=request.user)
        DentistProfileObj=DentistProfile.objects.get(user=request.user)   
        UserObj.first_name=first_name
        UserObj.last_name=last_name
        DentistProfileObj.title=title

        try:
            UserObj.save()
            DentistProfileObj.save()
            result = {"msg":"Success",}
        except:
            result = {"msg":"Failure",}
        return  result
                                      

@require_identity_type("Dentist")
@csrf_exempt
def upload_proof(request):
    '''
    Step中，医生上传identify图片时所用的Ajax接口
    '''
    BaseObj = Base.objects.get(user=request.user)
    template_var={}   
    if request.method=="POST":     
        DentistProfileObj=DentistProfile.objects.get(user=request.user)         
        if 'prove' in request.FILES:
            image = request.FILES["prove"]
            img= Image.open(image)
            ext = os.path.splitext(image.name)[1].split('.')[1]
            if ext=='jpg':
                ext='jpeg'
            elif ext=='JPG':
                ext='jpeg'
            out_im1 = cStringIO.StringIO()
            img.save(out_im1,ext)
            
            guid=gen_guid()
            filename='identify/'+'proof_'+guid
            _uptoS3([{
                    'filename': filename,
                    'filedir': out_im1
                }], ext)

            DentistProfileObj.prove_pic=filename
        else:
            image=None
        DentistProfileObj.prove_verify = 'S'
        DentistProfileObj.save()
        BaseObj.finish_steps = True
        BaseObj.save()
        return HttpResponseRedirect(reverse("to_homepage"))


@csrf_exempt
def save_img(request):
    '''
    保存用户上传头像时所用的Ajax接口。
    函数的主要功能是保存用户所上传的图片，并将保存之后的URL返回给前端用于预览显示.
    函数中还对用户是否在服务器端建立自己的用户文件进行了判断，若没有，则创建.
    但这个功能在以后的版本中应该单独拿出来，或放在更加适合的函数里面
    '''
    
    #上傳文件直接存放至S3服務器端，因此此處不再需要用戶文件夾
    # "make dir for the user if he have no dir"
    # new_path = os.path.join(settings.MEDIA_ROOT, request.user.username)
    # if not os.path.isdir(new_path):
    #     os.makedirs(new_path)    
    print("Start Upload")
    img_data = _imgupload(request,Base)
    if img_data["toolarge"]:
        print "size error"
        msg = "msg, Your img is too big"
        return HttpResponse(msg)

    else:
        url = settings.MEDIA_URL+img_data["url"]
        width = str(img_data["width"])
        height = str(img_data["height"])
        avatar = url +","+ width+","+ height
        print("Upload Over")

        return HttpResponse(avatar) 


@csrf_exempt
@ajax_request
def make_avatar(request):
    '''
    剪切头像时所用的Ajax接口。
    函数将用户上传的图片，按照前端传来的坐标位置剪切并保存
    '''

    result={
        'status': False,
        'msg': 'false'
    }
    data = json.loads(request.POST['data'])
    if 'x1' in data:
        print("Start Cut")
        _imgcut(request,Base,data)
        print("Cut Over")
        # print("Start shrink")
        # _imgshrink(request,Base)
        # print("Shrink Over")
        result = {
            'status': True,
            'msg': 'Success'
        }
    return result


def change_to_finished(request):
    '''
    Step步骤完成后，使用该函数修改finish_steps字段的值
    并调用to_homepage的连接跳转自相应的主页
    '''

    Base.objects.filter(user=request.user).update(finish_steps=True)
    return HttpResponseRedirect(reverse("to_homepage"))


@login_required
@render_to('accounts/settings.html')
def settingpage(request):

    BaseObj = Base.objects.get(user=request.user)
    try:
        DentistProfileObj = DentistProfile.objects.get(user=request.user)
        try:
            prove_pic = DentistProfileObj.prove_pic
        except:
            prove_pic = ""

        template_var = {
            "BaseObj": BaseObj,
            "prove_pic": prove_pic,
            "email_active": request.user.is_active,
            "site": request.META['HTTP_HOST']
        }
       
    except:
        template_var = {
            "BaseObj": BaseObj,
            "email_active": request.user.is_active,
            "site": request.META['HTTP_HOST']
        }
    finally:
        return template_var