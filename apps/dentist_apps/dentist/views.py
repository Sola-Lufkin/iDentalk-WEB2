# -*- coding: utf8 -*-
import re
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Max
#
from profile.models import Base, DentistProfile, PatientProfile, WorkPlace, TagList, Tag
from dentist.models import Qa
from den_profile.views import _get_den_info_
from den_manage.views import _get_patlist_info
from relationship.views import Relationship
from iDentalk import settings

from annoying.decorators import render_to, ajax_request
from django.utils import simplejson as json
from utils import JsonResponse
from decorators import *

@csrf_exempt
@login_required
def den_homepage(request,object_id=""):
    '''
    查看医生HomePage

    **参数**
    ``object_id``
        object_id默认或空字符串，代表所要返回的医生主页即为此时登录的医生的；
        object_id传入数字型的字符串，代表所要获取医生信息的id
    '''
    if object_id == "":
        template_var = _get_den_info_(request)
        WorkPlaceQuery = WorkPlace.objects.filter(dentistid=request.user.id)
        BaseObj = Base.objects.get(user=request.user)
        template_var["is_private"]=True

    else:
        ## 取消掉医生的第三人称视角的查看功能
        if int(object_id) == request.user.id:
            return HttpResponseRedirect(reverse("den_homepage"))      
        template_var =_get_den_info_(request,object_id)
        rel_status = -1
        is_patient = True   
        dentistuser = User.objects.get(id=object_id)
        DentistProfileObj = DentistProfile.objects.get(user=dentistuser)
        WorkPlaceQuery = WorkPlace.objects.filter(dentistid=dentistuser.id)
        BaseObj = Base.objects.get(user=dentistuser)
        
        print("是否是自己的主页:%s"%template_var["own"])
        # if template_var["own"]==True:
        #     print("欢迎，这里是您的主页！！")
        # else:
        print("该页面是否Pushed:%s"%DentistProfileObj.pushed)
        if DentistProfileObj.pushed:
            print("拥有者已经Push了他的主页，可以正常查看该页面")
            try:
                PatientProfileObj = PatientProfile.objects.get(user=request.user)
            except:
                is_patient= False
                print("妳不是病人，无权关注该医生")
        
            try:
                print("妳的注册身份是病人，妳现在可以关注或连接该医生了")
                RelationshipObj = Relationship.objects.get(patient = PatientProfileObj,dentist = DentistProfileObj )
                if RelationshipObj.status == 0:            
                    print("关注但未连接")
                    rel_status = 0
                elif RelationshipObj.status == 1:
                    print("已经向医生发出连接申请（默认关注）")
                    rel_status = 1
                elif RelationshipObj.status == 2:
                    print("已经连接（默认关注）")
                    rel_status = 2
            except:
                rel_status = -1 
        else:
            print("拥有者还未Push他的主页，将页面将跳转至页面错误提示")
            return Http404()

        template_var["is_private"]=False
        template_var['rel_status']=rel_status
        template_var['is_patient']=is_patient
        # template_var['pushed']=DentistProfileObj.pushed

    template_var["WorkPlaceQuery"]=WorkPlaceQuery
    template_var["BaseObj"]=BaseObj
    template_var["email_active"]=request.user.is_active
    template_var['user'] = request.user
    template_var['identity'] = Base.objects.get(user=request.user).identity
    template_var['avatar'] = settings.MEDIA_URL + str(Base.objects.get(user=request.user).imagesmall)

    if template_var["is_private"]:
        return render_to_response('dentist/homepage.html', template_var)
    else:
        return render_to_response('dentist/public_homepage.html', template_var)
    # return template_var
 

@render_to("dentist/pat_list.html")
@login_required
@require_identity_type('Dentist')
def pat_manage(request):
    return _get_patlist_info(request)


# return to mobile version
@render_to("mobile/m-pat_list.html")
@login_required
def pat_list(request):
    return _get_patlist_info(request)



# Q & A part
@csrf_exempt
def get_qa(request, uid):

    QaSet = Qa.objects.filter(user=User.objects.get(id=uid)).order_by('place')
    
    print "QaSet:", QaSet

    QaList = []
    for QaObj in QaSet:
        Qa_wrap = {}
        Qa_wrap = {
                'id': QaObj.id,
                'question': QaObj.question,
                'answer': QaObj.answer,
                'place': QaObj.place,
                'qa_owner_id': QaObj.user.id
        }

        QaList.append(Qa_wrap)
    print "QaList", QaList

    return JsonResponse(QaList)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def put_qa(request):
    data = json.loads(request.POST['data'])

    question = data['question'].strip()
    answer = data['answer'].strip()
    qa_owner_id = int(data['qa_owner_id'])

    qa_owner = User.objects.get(id=qa_owner_id)

    if request.user.id == qa_owner_id:
        if Qa.objects.filter(user=qa_owner).exists():
            max_place = Qa.objects.filter(user=qa_owner).aggregate(Max('place'))
            print "max_place", max_place
            QaObj = Qa(question=question, answer=answer, place=int(max_place['place__max'])+1, user=qa_owner)
            QaObj.save(force_insert=True)
        else:
            QaObj = Qa(question=question, answer=answer, place=1, user=qa_owner)
            QaObj.save(force_insert=True)

        result = {
                'id': QaObj.id,
                'question': QaObj.question,
                'answer': QaObj.answer,
                'place': QaObj.place,
                'qa_owner_id': QaObj.user.id,
                'msg': 'Success',
                }
        return JsonResponse(result)

    else:
        raise Http404


@csrf_exempt
# @require_http_methods(["POST"])
@login_required
def update_qa(request):
    data = json.loads(request.POST['data'])

    qa_id = data['id']
    question = data['question'].strip()
    answer = data['answer'].strip()
    qa_owner_id = int(data['qa_owner_id'])

    qa_owner = User.objects.get(id=qa_owner_id)

    if request.user.id == qa_owner_id:
        Qa.objects.filter(id=qa_id).update(question=question, answer=answer)
        QaObj = Qa.objects.get(id=qa_id)

        result = {
                'id': QaObj.id,
                'question': QaObj.question,
                'answer': QaObj.answer,
                'place': QaObj.place,
                'qa_owner_id': QaObj.user.id,
                'msg': 'Success',
                }
    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def move_qa_place(request):
    qa_id_group = request.POST['ids']
    print qa_id_group
    qa_id_list = re.split(',', qa_id_group)

    counter = 1
    for qa_id in qa_id_list:
        print "qa_id int: ", int(qa_id)
        Qa.objects.filter(id=int(qa_id)).update(place=counter)
        counter = counter + 1
        QaObj = Qa.objects.get(id=qa_id)

    result = {
            'msg': 'Success',
            }
    return JsonResponse(result)


@csrf_exempt
# @require_http_methods(["GET"])
@login_required
def delete_qa(request):
    qa_id = json.loads(request.POST['id'])

    Qa.objects.get(id=qa_id).delete()

    result = {
            'status': True,
            'msg': 'Deleted'
    }

    return JsonResponse(result)










# @login_required
# def den_homepage_pushed(request):
#     '''医生确定Push自己的页面'''
    
#     DentistProfileObj = DentistProfile.objects.get(user=request.user)
#     DentistProfileObj.pushed = True
#     DentistProfileObj.save()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# @login_required
# def den_homepage_pushed_cancel(request):
#     '''医生取消Push自己的页面'''
    
#     print("11")
#     DentistProfileObj = DentistProfile.objects.get(user=request.user)
#     DentistProfileObj.pushed = False
#     DentistProfileObj.save()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

##暂时无实用
# @csrf_exempt 
# @ajax_request
# def get_den_homepage(request, object_id = ""):

#     result = {}
#     print(request.user.id)
#     if object_id == "":
#         result = {"msg":"private page"}
#     else:
#         result = {"msg":"public page"}
#     return result    
