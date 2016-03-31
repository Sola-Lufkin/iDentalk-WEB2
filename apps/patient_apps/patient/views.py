# -*- coding: utf8 -*-
from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods 
#
from profile.models import Base, DentistProfile, PatientProfile, TagList, Tag
from django.contrib.contenttypes.models import ContentType
from pat_profile.views import _get_pat_info_
from pat_manage.views import _get_denlist_info
from annoying.decorators import render_to, ajax_request
from relationship.views import Relationship
from patient.models import Calendar
from notification.models import Event
from iDentalk import settings
from utils import JsonResponse
from decorators import require_identity_type
from django.utils import simplejson as json

@render_to("patient/homepage.html")
@login_required
def pat_homepage(request):
    ''''''
    template_var =_get_pat_info_(request)
    PatientProfileObj = PatientProfile.objects.get(user=request.user)
    BaseObj = Base.objects.get(user=request.user)

    template_var["PatientProfileObj"] = PatientProfileObj
    template_var["BaseObj"] = BaseObj
    template_var["denlist"] = _get_denlist_info(request)
    template_var["email_active"]=request.user.is_active
    print template_var["email_active"]
    return template_var


@render_to("mobile/m-den_list.html")
@login_required
def den_list(request):
    template_var =_get_pat_info_(request)
    template_var["denlist"] = _get_denlist_info(request)
    return template_var


@csrf_exempt
@render_to("patient/pathology.html")
@require_identity_type('Dentist')
@login_required
# FIXME
# 头像读取出错
# 判断是否是病人联系的医生 否则无法查看该页面
def pat_pathology(request,pid):

    template_var = {}
    PatientProfileObj = PatientProfile.objects.get(user=pid)
    dentists = [entry.dentist for entry in Relationship.objects.filter(patient=PatientProfileObj.user, status__gt=0)]

    if DentistProfile.objects.get(user=request.user) in dentists : # 这个用户所关注的人 
        template_var =_get_pat_info_(request,object_id=pid)
        BaseObj = Base.objects.get(user=pid)
        template_var["PatientProfileObj"] = PatientProfileObj
        template_var["BaseObj"] = BaseObj
    else:
        return HttpResponseRedirect('/error')
    return template_var


@csrf_exempt
@render_to("patient/pathology.html")
@login_required
def pat_dental_record(request):

    template_var = {}
    PatientProfileObj = PatientProfile.objects.get(user=request.user.id)
    template_var =_get_pat_info_(request,object_id=request.user.id)
    BaseObj = Base.objects.get(user=request.user)
    template_var["PatientProfileObj"] = PatientProfileObj
    template_var["BaseObj"] = BaseObj
    template_var["own"] = True
    return template_var


@render_to("patient/calendar.html")
@login_required
def calendar(request, pid):
    if request.user.id == int(pid):
        try:
            '''
                Mark all calendar notice as read
            '''
            calendar_type_object = ContentType.objects.get(model='calendar')
            event = Event.objects.filter(user=request.user, content_type=calendar_type_object)
            event.update(seen=True)
        except: 
            pass
        finally:
            patient_name = request.user.last_name

            template_var = {
                'p_name': patient_name
            }

            return template_var
    else:
        raise Http404
        # BaseObj = Base.objects.get(user=request.user) # noware calendar request user

        # if BaseObj.identity != 'D':
        #     print "other Patient"
        #     return HttpResponseRedirect('/error')
        # else:
        #     PatientProfileObj = PatientProfile.objects.get(user=User.objects.get(id=pid))
        #     print PatientProfile
        #     connectted = [entry.dentist for entry in Relationship.objects.filter(patient=PatientProfileObj, status=2)]
        #     print connectted

        #     if DentistProfile.objects.get(user=BaseObj) not in connectted:
        #         raise Http404 # should be 'You request page not found'
        #     else:
        #         template_var = {
        #                         'p_name': User.objects.get(id=pid).last_name
        #         }
        #         print "Connected Dentist"

        #         return template_var


@require_http_methods(["POST"])
@csrf_exempt
@login_required
def get_calendar(request):

    start = request.POST['start']
    end = request.POST['end']
    pid = request.POST['pid']
   
    nowa_start = datetime.utcfromtimestamp(int(start))
    nowa_end = datetime.utcfromtimestamp(int(end))


    CalendarSet = Calendar.objects.filter(patient=User.objects.get(id=pid),start__gte=nowa_start,
                                        end__lte=nowa_end)
    print "CalendarSet:", CalendarSet

    CalendarList = []
    for CalendarObj in CalendarSet:
        Calendar_wrap = {}
        Calendar_wrap = {
                        'id': CalendarObj.id,
                        'title': CalendarObj.title,
                        'content': CalendarObj.content,
                        'start': str(CalendarObj.start),
                        'end': str(CalendarObj.end),
                        'color': CalendarObj.color,
                        'dentist': {
                            'id': CalendarObj.dentist_id,
                            'name': ''
                        }
                        # 'patient': CalendarObj.patient,
        }

        CalendarList.append(Calendar_wrap)
    print "CalendarList", CalendarList

    return JsonResponse(CalendarList)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def put_calendar(request):
    data = json.loads(request.POST['data'])

    try:
        title = data['title'].strip()
    except:
        title = data['content'].strip()[:20]
    content = data['content'].strip()
    start = data['start']
    try:
        end = data['end']
    except:
        end = start
    try:
        pid = data['pid']
    except:
        pid = data['contact-id']
    patient = PatientProfile.objects.get(user=User.objects.get(id=pid))
    # start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    # end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')

    if request.user.id == int(pid):
        CalendarObj = Calendar(title=title, content=content, start=start, end=end, color='blue', patient=patient)
        CalendarObj.save(force_insert=True)

        result = {
                'id': CalendarObj.id,
                'title': CalendarObj.title,
                'content': CalendarObj.content,
                'start': CalendarObj.start,
                'end': CalendarObj.end,
                'dentist': {
                    'name': ''
                }
        }

        return JsonResponse(result)

    else:
        BaseObj = Base.objects.get(user=request.user) # noware calendar request user

        if BaseObj.identity != 'D':
            print "other Patient"
            return HttpResponseRedirect('/error')
        else:
            PatientProfileObj = PatientProfile.objects.get(user=User.objects.get(id=pid))
            connectted = [entry.dentist for entry in Relationship.objects.filter(patient=PatientProfileObj, status=2)]
            print connectted

            if DentistProfile.objects.get(user=BaseObj) not in connectted:
                raise Http404 # should be 'You request page not found'
            else:
                CalendarObj = Calendar(title=title, content=content, start=start, end=end, color='red', dentist_id=request.user.id, patient=patient)
                CalendarObj.save(force_insert=True)
                
        return JsonResponse({})


@csrf_exempt
# @require_http_methods(["POST"])
@login_required
def update_calendar(request):
    data = json.loads(request.POST['data'])

    cal_id = data['id']
    title = data['title'].strip()
    content = data['content'].strip()
    start = data['start']
    end = data['end']

    if end == '':
        end = start

    Calendar.objects.filter(id=cal_id).update(title=title, content=content, start=start, end=end)

    result = {
            'id': cal_id,
            'title': title,
            'content': content,
            'start': start,
            'end': end,
    }

    return JsonResponse(result)


@csrf_exempt
# @require_http_methods(["GET"])
@login_required
def delete_calendar(request):
    data = json.loads(request.POST['id'])

    cal_id = data
    Calendar.objects.get(id=cal_id).delete()

    result = {
            'status': True,
            'msg': 'Success'
    }

    return JsonResponse(result)
