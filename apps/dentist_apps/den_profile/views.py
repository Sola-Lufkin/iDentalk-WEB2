# -*- coding: utf8 -*-
import decimal
import os
import Image
from utils import gen_guid
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User   
from django.utils.translation import ugettext_lazy as _ 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from profile.forms import *
from den_manage.views import _relation_counts
from decorators import require_identity_type

from profile.models import *
from public.views import _show_name, _show_obj_name, _count_age, to_homepage
import settings
from imgupload.views import _uptoS3

from annoying.decorators import ajax_request
from annoying.decorators import render_to
from utils import JsonResponse, json_serialize
from django.utils import simplejson as json
import cStringIO


def _tag_get(request,tagtype,object_id=""):
    '''
    读取登录用户（身份医生）的Feild和Degree标签

    **参数**
    ``tagtype``
        tagtype为tag的类别
    '''
    if object_id =="":
        # DentistProfileObj = DentistProfile.objects.get(user = request.user)
        TagListQuery = TagList.objects.filter(dentistid = request.user.id, tagtype = tagtype)
    else:
        TagListQuery = TagList.objects.filter(dentistid = object_id, tagtype = tagtype)
    TagQuery = Tag.objects.filter(tagtype = tagtype)

    A = []
    for i in TagListQuery:
        A.append(i.tagid)

    UnChoice_List = []
    Choice_List = []
    for i in TagQuery:
        if i in A:
            Choice_List.append({'id':i.id,'name':i.name,})
        else:
            UnChoice_List.append({'id':i.id,'name':i.name,})

    return Choice_List, UnChoice_List


@login_required
@require_http_methods(['POST']) 
@csrf_exempt
@ajax_request
def den_pro_Tag_edit(request, tagtype):
    '''
    添加和修改Field或Degree标签 数据存储接口

    ***
    ``tagtype``
        tagtype为tag的类别，在urls.py里被赋值，并传入该函数
    '''
    
    result = { 'msg':'failure', 'status':0, }                        
    DentistProfileObj = DentistProfile.objects.get(user=request.user)
    tags = request.POST['tags']
    if tags == "":
        TagList.objects.filter(dentistid=DentistProfileObj,tagtype=tagtype).delete()
        result = { 'msg':'Success', 'status':1}
    else:
        taglist = tags.split(',')
        DentistProfileObj.feild_count = len(taglist)
        feild_count = len(taglist)
            
        print("用户录入的标签个数为：%s")%(feild_count)

        TagList.objects.filter(dentistid=DentistProfileObj,tagtype=tagtype).delete()
        i = 0
        while i < feild_count:
            
            try:
                TagObj = Tag.objects.get(name = taglist[i], tagtype = tagtype)
                print("Tag库%s类中存在[%s]标签")%(tagtype,TagObj)
                TagList(tagid=TagObj, tagtype = TagObj.tagtype, dentistid=DentistProfileObj).save()                    
                print("为该用户关联该标签")
                                
            except:
                print("Tag库%s类中不存在该标签")%(tagtype)
                Tag(name = taglist[i], verify = 0, tagtype = tagtype).save()            
                TagObj = Tag.objects.get(name = taglist[i] ,tagtype = tagtype) 
                print("Tag库%s类中创建[%s]标签")%(tagtype,TagObj)               
                TagList(tagid=TagObj, tagtype = TagObj.tagtype, dentistid=DentistProfileObj).save()           
                print("为该用户关联该标签") 
            i=i+1    
        try:  
            DentistProfileObj.save()
            result = { 'msg':'Success', 'status':1}
        except:
            result = { 'msg':'Failure', 'status':0}

    return result
  

def _get_den_info_(request,object_id = ""):
    '''
    该函数获取医生的个人信息，并包装成包

    **参数**
    ``object_id``
        object_id默认或空字符串，代表所要获取的医生信息即为此时登录的医生的信息；
        object_id传入数字型的字符串，代表所要获取医生信息的id
    '''

    template_var = {}
    myname = ""
    objname = ""
    if object_id == "":
        myname = _show_name(request)       
        UserObj = User.objects.get(username=request.user)
        BaseObj = Base.objects.get(user=request.user)
        DentistProfileObj = DentistProfile.objects.get(user=request.user)
        WorkPlaceQuery = WorkPlace.objects.filter(dentistid=request.user.id)
        choice_feild, unchoice_feild = _tag_get(request,tagtype="F")
        choice_degree, unchoice_degree = _tag_get(request,tagtype="D")
        ##
        counts = _relation_counts(request)
    else :
        objname = _show_obj_name(object_id) 
        UserObj = User.objects.get(id=object_id)
        BaseObj = Base.objects.get(user=UserObj)
        DentistProfileObj = DentistProfile.objects.get(user=UserObj) 
        WorkPlaceQuery = WorkPlace.objects.filter(dentistid=UserObj.id)
        choice_feild, unchoice_feild = _tag_get(request,tagtype="F",object_id=object_id)
        choice_degree, unchoice_degree = _tag_get(request,tagtype="D",object_id=object_id)
        ##
        counts = _relation_counts(request,dentistid=DentistProfileObj.user.user.id, patientid=request.user.id)    
        
    own=False
    if UserObj == request.user:
        own=True
    title = DentistProfileObj.title
    
    if title == "1":
        title_var = "Dr."
    elif title == "2":
        title_var = "Prof."
    elif title == "3":
        title_var = "Mr."
    elif title == "4":
        title_var = "Ms."
    elif title == "5":                    
        title_var = "Dr(Prof)." 

    # print counts["status"]
    # print counts["patient_count"]
    # print counts["follower_count"]
    
    Info = {
            "username":UserObj.username,
            "first_name":UserObj.first_name,
            "last_name":UserObj.last_name,
            # "middle_name":BaseObj.middle_name,
            # "show_mid_name":BaseObj.show_mid_name,
            "title":DentistProfileObj.title,
            "imagephoto":BaseObj.imagephoto.url,
            "imagebig":BaseObj.imagebig.url,
            "imagesmall":BaseObj.imagesmall.url,
            "summary":BaseObj.summary,
            "workemail":BaseObj.workemail,
            "same_account_email":BaseObj.same_account_email,
            ## 医生的热度值，包括follower人数和pateint 人数
            "patient_count":counts["patient_count"],
            "follower_count":counts["follower_count"],
           }

    WorkPlaceList = []
    for i in WorkPlaceQuery:
        DATE_FORMAT = "%H:%M"
           
        try:
            business_hour = i.business_hour
        except:
            business_hour = ""
        
        WorkPlaceInfo = {
                'id':i.id,
                'clinic_name':i.clinic_name,
                'location':i.location,
                'latitude': str(i.latitude),
                'longitude': str(i.longitude),
                #'postcode':i.postcode,
                'tel':i.tel,
                'business_hour': business_hour,
        }
        WorkPlaceList.append(WorkPlaceInfo)

    template_var = {
                'Info':Info,
                'title_var':title_var,
                'myname':myname,
                'objname':objname,
                'WorkPlaceList':WorkPlaceList,
                'choice_feild':choice_feild,
                'unchoice_feild':unchoice_feild,
                'choice_degree':choice_degree,
                'unchoice_degree':unchoice_degree,
                'own':own,
                'object_id':object_id,
                # 'pushed':DentistProfileObj.pushed,
                 }

    return template_var


@login_required
@require_http_methods(['POST'])
@csrf_exempt
@ajax_request
def den_pro(request,object_id=""):
    '''
    医生的profile页 数据获取接口

    **参数**
    ``object_id``
        object_id默认或空字符串，代表所要获取的医生信息即为此时登录的医生的信息；
        object_id传入数字型的字符串，代表所要获取医生信息的id
    '''

    if object_id == "":
        template_var=_get_den_info_(request)
        return JsonResponse(template_var)
    else:
        template_var = _get_den_info_(request,object_id)
        return template_var
  
 
@login_required
@require_http_methods(['POST'])
@csrf_exempt
@ajax_request
def den_pro_base(request):
    '''医生的基本信息填写 数据存储接口'''

    result = { "msg":"failure", "status":0 }      
    data = json.loads(request.POST['data'])
    '''
    前端使用Ajax遍历，show_mid_name未选中时，
    并不会传值过来，需要后端使用try方法手动赋值
    '''
    if 'same_account_email' in data:
        # show_mid_name=data["show_mid_name"]
        same_account_email=True
        workemail = request.user.username
    else:
        # show_mid_name=False
        same_account_email=False
        workemail = data["workemail"].strip()

    try:
        User.objects.filter(username=request.user).update(
                                                          first_name=data["first_name"].strip(),
                                                          last_name=data["last_name"].strip(),
                                                         )

        Base.objects.filter(user=request.user).update(
                                                      # middle_name=data["middle_name"],
                                                      # show_mid_name=show_mid_name,
                                                      same_account_email=same_account_email,
                                                      workemail=workemail,
                                                      summary=data["summary"].strip(),
                                                      )

        DentistProfile.objects.filter(user=request.user).update(title=data["title"],)
        result = {"msg":"Success", "status":1}
    except:
        result = {"msg":"Failure", "status":0}

    return result
            

@login_required
@csrf_exempt   
def den_pro_loc_add(request):
    '''当前登录用户（身份医生）的地址信息添加 函数会返回HTML页面'''

    DentistProfileObj = DentistProfile.objects.get(user=request.user)
    if DentistProfileObj.workplace_count < 3:
        template_var={}
        form = DentistProfileLocForm()

        if request.method=="POST": 
            try:
                data = json.loads(request.POST['data'])
                print data["latlng"]
                if data['latlng'] == '':
                    latitude = longitude = 0 
                else:
                    latlng = data["latlng"].replace("(",'').replace(")",'').split(', ')

                    ## fill the latlng
                    latitude = decimal.Decimal(latlng[0])
                    longitude = decimal.Decimal(latlng[1])

                print latitude
                print longitude

                try:
                    WorkPlace(clinic_name = data["clinic_name"].strip(),
                              location = data["location"].strip(),
                              latitude = latitude,
                              longitude = longitude,
                              #postcode = data["postcode"],
                              tel = data["tel"].strip(),
                              business_hour = data["business_hour"].strip(),
                              dentistid = DentistProfileObj
                              ).save()

                except:
                    WorkPlace(clinic_name = data["clinic_name"].strip(),
                              location = data["location"].strip(),
                              latitude = latitude,
                              longitude = longitude, 
                              #postcode = data["postcode"],
                              tel = data["tel"].strip(),
                              dentistid = DentistProfileObj
                              ).save()
            
                DentistProfileObj.workplace_count = DentistProfileObj.workplace_count + 1
                DentistProfileObj.save()
                result = { "msg":"Success", "status":1,}
                return JsonResponse(result)

            except:
                result = { "msg":"Failure", "status":0,}
                return JsonResponse(result)             
        else:
            template_var= {
                            "form":form,
                            "method":"add",
                          }
            return render_to_response("profile/dentist_pro/dentist_location.html",
                                      template_var,
                                      context_instance=RequestContext(request)
                                     )
    else:
        #如果workplace_count大于3，则提醒用户不可以再添加
        result = "Sorry, You had already added 3 locations!"
        return JsonResponse(result)
    

@login_required
@csrf_exempt
def den_pro_loc_edit(request,object_id):
    '''当前登录用户（身份医生）的地址信息修改 函数会返回HTML页面'''
        
    if request.method=="POST": 
        try:    
            data = json.loads(request.POST['data'])
            ## start&&end is not necessary, use try to make it work

            latlng = data["latlng"].replace("(",'').replace(")",'').split(', ')
            latitude = decimal.Decimal(latlng[0])
            longitude = decimal.Decimal(latlng[1])
            print latitude
            print longitude

            try:
                WorkPlace.objects.filter(id=object_id).update(
                                                                clinic_name = data["clinic_name"].strip(),
                                                                location = data["location"].strip(),
                                                                latitude = latitude,
                                                                longitude = longitude,
                                                                #postcode = data["postcode"],   
                                                                tel = data["tel"].strip(),
                                                                business_hour = data["business_hour"].strip(),
                                                              )
            except:
                WorkPlace.objects.filter(id=object_id).update(
                                                                clinic_name = data["clinic_name"].strip(),
                                                                location = data["location"].strip(),
                                                                latitude = latitude,
                                                                longitude = longitude,   
                                                                #postcode = data["postcode"],   
                                                                tel = data["tel"].strip(),
                                                             )
            result = {
                        "msg":"Success",
                        "status":1,
                        }
                        
            return JsonResponse(result)

        except:

            result = {
                        "msg":"Failure",
                        "status":0,
                        }
            return JsonResponse(result)

    else:
        WorkPlaceObj = WorkPlace.objects.get(id=object_id)

        latitude = str(WorkPlaceObj.latitude)
        longitude = str(WorkPlaceObj.longitude)
        latlng = "("+latitude+", "+longitude+")"

        form = DentistProfileLocForm()                 
        template_var={"form":form,
                      "WorkPlaceObj":WorkPlaceObj,
                      "latlng": latlng,
                      "method":"edit",
                     }

        return render_to_response("profile/dentist_pro/dentist_location.html",
                                  template_var,
                                  context_instance=RequestContext(request)
                               )
   

@login_required
@require_http_methods(['POST'])
@csrf_exempt
@ajax_request
def den_pro_loc_delete(request,object_id):
    '''删除当前登录用户（身份医生）的地址信息 功能接口'''

    DentistProfileObj = DentistProfile.objects.get(user=request.user)
    
    WorkPlace.objects.get(id=object_id).delete()
    DentistProfileObj.workplace_count = DentistProfileObj.workplace_count - 1
    DentistProfileObj.save()
    result = {
            'msg': 'Success',
            'status': 1
    }
    return result


@csrf_exempt
@login_required
@require_http_methods(['GET', 'POST'])
@require_identity_type("Dentist")
def add_prove_pic(request):
    """ this function is to serve Prove Picture Upload Page """

    BaseObj = Base.objects.get(user=request.user)

    DentistProfileObj=DentistProfile.objects.get(user=request.user)

    try:
        image = request.FILES["prove_pic"]

    except Exception, e:
        prove_pic = ""
        template_var = {
            "prove_pic": prove_pic
        }

    else:
        img= Image.open(image)
        ext = os.path.splitext(image.name)[1].split('.')[1]
        if ext=='jpg':
            ext='jpeg'
        elif ext=='JPG':
            ext='jpeg'
        out_im1 = cStringIO.StringIO()
        img.save(out_im1, ext)
        
        guid=gen_guid()
        filename = 'identify/proof_' + guid
        _uptoS3([
            {
                'filename': filename,
                'filedir': out_im1
            }
            ], ext)

        DentistProfileObj.prove_pic = settings.MEDIA_URL + filename
        DentistProfileObj.prove_verify = 'S'
        DentistProfileObj.save()
        BaseObj.save()

        template_var = {
            # "identity": BaseObj.identity,
            "prove_pic": settings.MEDIA_URL + filename
        }

    finally:
        return HttpResponse(settings.MEDIA_URL + filename)
