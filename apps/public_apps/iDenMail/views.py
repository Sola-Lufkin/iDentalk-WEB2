# -*- coding: utf8 -*-
import os
import random
import string
import datetime
from time import *
import Image
from Image import EXTENT
#
from django.core.paginator import Paginator,InvalidPage,EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User   
from django.utils.translation import ugettext_lazy as _ 
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json
from utils import JsonResponse, json_serialize, humantime
#
from profile.models import *
from iDentalk import settings
from iDentalk.decorators import require_identity_type, steps_require_unfinished
from annoying.decorators import render_to, ajax_request
from iDenMail.models import *
from iDenMail.forms import MailForm

# from relationship.models import Relationship
from den_manage.views import _get_patlist_info
from pat_manage.views import _get_denlist_info
from public.views import _show_name, _show_obj_name
from patient.views import put_calendar


@csrf_exempt
@ajax_request
@login_required
def post_mail(request):
    result = {}

    try:
        data = json.loads(request.POST['data'])
        uid = data['contact-id']
        content = data['content']
        start = data['start']
        calendar_time = data['time']
        if start or calendar_time:
            content = content.strip() + '.\n#calendar' + start + ' ' + calendar_time
            put_calendar(request)
            m_type = 3
            print "put calendar"
        else:
            print "mail start"
            content = content.strip()
            m_type = 0

        if len(content) > 600:
            result = {
                "status": False,
                "msg": "At most enter 600 characters."
            }

    except:
        data = json.loads(request.POST['data'])
        uid = data['contact-id']
        content = data['content']
        m_type = 0

    finally:
        UserObj = User.objects.get(username=request.user)
        ReceiveQuery = User.objects.filter(id=uid)

        MailTextNew = MailText(content = content, type = m_type, sender = UserObj)
        MailTextNew.save()

        MailInfoNew = MailInfo(mailtext = MailTextNew, post_date = MailTextNew.post_date,
                                status = 0, receiver = User.objects.get(id=uid))
        MailInfoNew.save()
        result = {
            "msg":"Success",
            "status": True,
        }
        return result


@render_to("iDenMail/mails.html")
@login_required
def mails(request):

    template_var = {}
    try:
        if Base.objects.get(user=request.user).identity == "D":
            template_var = {
                        "contacter_list":_get_patlist_info(request)["Connected_List"],
                        "dentist":True,
        }
        else:
            template_var = {
                        "contacter_list":_get_denlist_info(request)["Connected_List"],
                        "dentist":False,
        }
    except:
        pass
        
    return template_var


@render_to("iDenMail/mail_history.html")
@login_required
def mail_history(request,object_id):

    UserObj =User.objects.get(username = request.user)
    contacter = User.objects.get(id = object_id)

    UserInfo =Base.objects.get(user=UserObj)
    contacterInfo =Base.objects.get(user=contacter)

    mails = [entry.mailtext for entry in MailInfo.objects.filter(receiver = UserObj)]
    mails_a = [entry.mailtext for entry in MailInfo.objects.filter(receiver = contacter)]

    mails_received = []
    mails_sended = []
    DATE_FORMAT = "%Y%m%d%H%M%s"
    for i in mails:
        if i.sender == contacter:
            MailInfo.objects.filter(receiver=UserObj,mailtext=i).update(status=1) #标记为已读
            time_reminder = i.content.find('#calendar')
            if time_reminder != -1:
                reminder = i.content[time_reminder+9:]
            else:
                reminder = ''
            mail = {
                # "sender":json_serialize(i.sender),
                "name":_show_obj_name(object_id),
                "avatar": settings.MEDIA_URL + str(contacterInfo.imagesmall),
                "uid":UserObj.id,
                "content":i.content[:time_reminder],
                "type": i.type,
                "reminder": reminder,
                "date":str(i.post_date),
                "humandate":humantime(i.post_date),
                "int_date": mktime(i.post_date.timetuple()),
                "own":False,
            }
            mails_received.append(mail)

    for i in mails_a:
        if i.sender == UserObj:
            time_reminder = i.content.find('#calendar')
            if time_reminder != -1:
                reminder = i.content[time_reminder+9:]
            else:
                reminder = ''
            mail = {
                # "sender":json_serialize(i.sender),
                "name":_show_name(request),
                "avatar": settings.MEDIA_URL + str(UserInfo.imagesmall),
                "uid":UserObj.id,
                "content":i.content[:time_reminder],
                "type": i.type,
                "reminder": reminder,
                "date":str(i.post_date),
                "humandate":humantime(i.post_date),
                "int_date": mktime(i.post_date.timetuple()),
                "own":True,
        }
            mails_sended.append(mail)
    mail_history = mails_received + mails_sended
    mail_history.sort(cmp=lambda x,y:cmp(y["int_date"],x["int_date"]))

    paginator = Paginator(mail_history,10)  ##分页处理
    try:
        page = int(request.GET.get('page','1'))
    except Valueerrors:
        page = 1
    try:
        mail_per_page = paginator.page(page)
    except(EmptyPage,InvalidPage):
        mail_per_page = paginator.page(paginator.num_pages)

    if Base.objects.get(user=UserObj).identity == "D":
        template_var = {
        
                'mail_per_page':mail_per_page,
                'mail_history': mail_history,
                'contacter_list':_get_patlist_info(request)["Connected_List"],
                'uid':object_id,
                'dentist':True,
                'name':_show_obj_name(object_id),
        } 
    else:
        template_var = {
        
                'mail_per_page':mail_per_page,
                'mail_history': mail_history,
                'contacter_list':_get_denlist_info(request)["Connected_List"],
                'uid':object_id,
                'dentist':False,
                'name':_show_obj_name(object_id),
        } 
    
    return template_var


# @render_to("iDenMail/mails.html")
# def latest_mails(request):

#     UserObj =User.objects.get(username = request.user)
#     latest_mails = []
#     for i in [entry.mailtext for entry in MailInfo.objects.filter(receiver = UserObj).order_by('post_date')[:10]]:
#         mail={
#             "sender":i.sender,
#             "content":i.content,
#             "date":i.post_date,
#         }
#         latest_mails.append(mail)
#     template_var = {
#                     "contacter_list":_get_patlist_info(request,"Connected")["Connected_List"],
#                     "latest_mails":latest_mails,
#     }
#     return template_var


# @render_to("iDenMail/post_mail.html")
# def post_mail(request):

#     template_var = {}
#     form = MailForm()

#     if request.method=="POST":
#         form = MailForm(request.POST)
#         print("Start")
#         if form.is_valid():
#             content = form.cleaned_data['content']
#             UserObj = User.objects.get(username = request.user)
#             ReceiveObj = User.objects.get(username = form.cleaned_data['username'])
#             ReceiveQuery = User.objects.filter(username = form.cleaned_data['username'])
#             MailTextNew = MailText(content = content,
#                                    type = 0,
#                                    sender = UserObj,

#                                   )
#             MailTextNew.save()
#             print("MailTextNew Saved")
#             MailInfoNew = MailInfo(mailtext = MailTextNew,
#                                    status = 0,
#                                    receiver = ReceiveObj,

#                                   )
#             MailInfoNew.save()

            
#             print("AX")
#             notification.observe(MailInfoNew,UserObj,"friends_accept")
#             print("BX")


#             notification.send( 
#                                 users=ReceiveQuery,
#                                 label="friends_invite", 
#                                 extra_context={"from_user": UserObj.username,"user_id":UserObj.id},
#                                 sender=UserObj,
#                                 # queue=True,
#                              )
#             print("MailInfoNew Saved")

#     template_var = {
#                     "form":form,

#     }

#     return template_var


# @render_to("iDenMail/mail_list.html")
# def mail_list(request):

#     template_var = {}
#     UserObj = User.objects.get(username = request.user)
#     MailInfoQuery = MailInfo.objects.filter(receiver = UserObj)


#     print notification.should_send(request.user, NoticeType.objects.get(label="friends_accept"), "1")
#     NoticeQuery = Notice.objects.filter(recipient = UserObj)
#     print (NoticeQuery)
#     print Notice.objects.unseen_count_for( recipient = request.user)
#     template_var = {
#                     # "MailInfoQuery":MailInfoQuery,
#                     "NoticeQuery":NoticeQuery

#     }
#     return template_var


# @render_to("iDenMail/mail_detail.html")
# def mail_detail(request, object_id=""):

#     template_var = {}
#     MailTextObj = MailText.objects.get(id = object_id)
#     print MailTextObj.content
#     print MailTextObj.post_date

#     template_var = {
#                     "MailTextObj":MailTextObj,
#     }
#     return template_var


# @ajax_request
# def mail_Listener(request):

#     result = {}
#     UserObj = User.objects.get(username = request.user)
#     count = 0
#     MailInfoQuery = []
#     for i in MailInfo.objects.filter(receiver = UserObj, status = 0):
#         count = count +1
#         a = {
#             "content":i.mailtext.content,
#             "post_date":str(i.mailtext.post_date),

#         }
#         MailInfoQuery.append(a)

#     LatestMailInfo = MailInfoQuery[count-1]
#     result = {
#                 "count":count,
#                 # "lastmail":LatestMailInfo.mailtext.content,
#                 # "post_date":str(LatestMailInfo.mailtext.post_date),
#                 "MailInfoQuery":MailInfoQuery,
#     }
#     return result


# @render_to("iDenMail/timeline.html")
# def main(request):

#     template_var = {}
#     user = User.objects.get(username=request.user) # 某个用户
#     followers = [entry.dentist for entry in Relationship.objects.filter(patient=user)] # 这个用户所关注的人
     
#     events = ObservedItem.objects.filter(user__in=followers)

#     print(events)
#     template_var = {
#                     'events': events ,

#     }
     
#     return template_var
