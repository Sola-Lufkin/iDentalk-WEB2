# coding=utf-8
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#
from django.contrib.contenttypes.models import ContentType
from relationship.models import Relationship
from profile.models import Base
from stream.models import *
from patient.models import Calendar
from notification.models import Event
from public.views import _show_obj_name
from annoying.decorators import ajax_request
#
from iDentalk import settings
from django.utils import simplejson as json
from utils import JsonResponse, json_serialize


"""
select content type Object from ContentType Table for global use.
"""
comment_type_object = ContentType.objects.get(model='comment')
relation_type_object = ContentType.objects.get(model='relationship')
mailinfo_type_object = ContentType.objects.get(model='mailinfo')
calendar_type_object = ContentType.objects.get(model='calendar')


@csrf_exempt
@require_http_methods(["GET"])
@login_required
def notice_get(request):
    """ 
    select Event Object from Event Table, and render to notifications.html page to display.
    @version 0.5
    """

    user = request.user
    BaseObj = Base.objects.get(user=user)

    if BaseObj.identity == 'D':

        request_id_collect = [entry.id for entry in Relationship.objects.filter(dentist=user, status=1)]
        D_RequestSet = Event.objects.filter(content_type=relation_type_object, object_id__in=request_id_collect, archived=False).order_by('-id')


        # post_id_collect = [entry.id for entry in Post.objects.filter(user_id=user)]
        # comment_id_collect = [entry.id for entry in Comment.objects.filter(post_id__in=post_id_collect)]#user__in = followers, 
        # StreamE = Event.objects.filter(content_type=comment_type_object, object_id__in=comment_id_collect)
        # print StreamE
        # these operation result equal these below

        StreamEventDict = Event.objects.filter(content_type=comment_type_object).order_by('-id') #'all comment'
        StreamEvent_wrap = [] # to filter which comment belong to now dentist's post

        for StreamEventObj in StreamEventDict:
            if StreamEventObj.event_object.post_id.user_id != user:
                # print 'continue the next loop'
                continue
            else:
                StreamEvent_wrap.append(StreamEventObj)

        result = {
                "StreamEventDict": StreamEvent_wrap,
                "D_RelationEventDict": D_RequestSet,
                "imagesmall": settings.MEDIA_URL + str(BaseObj.imagesmall),
                "identity": 'D'
                }

    else:
        request_id_collect = [entry.id for entry in Relationship.objects.filter(patient=user, status=2)]
        P_RequestSet = Event.objects.filter(content_type=relation_type_object, object_id__in=request_id_collect, archived=False).order_by('-id')

        result = {
                "P_RelationEventDict": P_RequestSet,
                "identity": 'P'
                }

    return render_to_response('notification/notifications.html', result,
                          context_instance=RequestContext(request))


def _msg_count(request):
    """ return count for call function 'remind_count'. """

    UserObj = User.objects.get(username=request.user)
    count = 0
    count = Event.objects.filter(user=UserObj, seen=False, content_type=mailinfo_type_object).count()

    return count


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def remind_count(request):
    """
    notice listen, then return count number of notice or message
    @version 0.4
    """

    user = request.user
    count = 0
    BaseObj = Base.objects.get(user=user)

    if BaseObj.identity == 'D':

        # followers = [entry.patient for entry in Relationship.objects.filter(dentist=user)]
           # in Event table will filter the same patient name which not belong to now dentist.
        # D_NoticeDict_count = Event.objects.filter(user__in = followers, content_type__in = content_type_list)
        request_id_collect = [entry.id for entry in Relationship.objects.filter(dentist=user, status=1)]
        request_count = Event.objects.filter(content_type=relation_type_object, object_id__in=request_id_collect, seen=False).count()

        StreamEventDict = Event.objects.filter(content_type=comment_type_object, seen=False) #'all comment'
        StreamEvent_wrap = [] # to filter which comment belong to now dentist's post

        for StreamEventObj in StreamEventDict:
            if StreamEventObj.event_object.post_id.user_id != user:
                continue
            else:
                StreamEvent_wrap.append(StreamEventObj)

        comment_count = len(StreamEvent_wrap)
        print('comment count: %s' % comment_count)

        result = {
                "notice_count": request_count+comment_count,
                "msg_count": _msg_count(request)
        }

    else:
        request_id_collect = [entry.id for entry in Relationship.objects.filter(patient=user, status=2)]
        pat_list = [entry.id for entry in Calendar.objects.filter(patient=user)]
        request_count = Event.objects.filter(content_type=relation_type_object, object_id__in=request_id_collect, seen=False).count()
        calendar_count = Event.objects.filter(content_type=calendar_type_object, object_id__in=pat_list, seen=False).count()

        result = {
                "notice_count": request_count,
                "msg_count": _msg_count(request),
                "cal_count": calendar_count
        }

    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["GET"])
@login_required
def notice_click(request):
    """
    Set db content_type=comment 'seen' field to 'True', and clean the number of notice button. 
    @version 0.4
    """

    user = request.user
    BaseObj = Base.objects.get(user=user)
    content_type_list = [comment_type_object, relation_type_object]
    
    if BaseObj.identity == 'D':

        request_id_collect = [entry.id for entry in Relationship.objects.filter(dentist=user, status=1)]
        Event.objects.filter(content_type=relation_type_object, object_id__in=request_id_collect, seen=False).update(seen=True)

        StreamEventDict = Event.objects.filter(content_type=comment_type_object, seen=False) #'all comment'
        # to filter which comment belong to now dentist's post

        for StreamEventObj in StreamEventDict:
            if StreamEventObj.event_object.post_id.user_id != user:
                continue
            else:
                StreamEventObj.seen=True
                StreamEventObj.save()
                
    else:
        # following = [entry.dentist for entry in Relationship.objects.filter(patient=user)]
        # Event.objects.filter(user__in = following, content_type=relation_type_object, seen=False).update(seen=True)
        request_id_collect = [entry.id for entry in Relationship.objects.filter(patient=user, status=2)]
        Event.objects.filter(content_type=relation_type_object, object_id__in=request_id_collect, seen=False).update(seen=True)

    return HttpResponseRedirect(reverse("notice"))


def notice_archive(request, object_id):
    """ Let patient archived the request success notifications. @version 0.2 """

    print object_id
    try:
        Event.objects.filter(id=object_id).update(archived=True)
        # print 'success'
    except:
        # print 'error'
        pass

    return HttpResponseRedirect(reverse("notice"))


@csrf_exempt
@ajax_request
@require_http_methods(["POST"])
@login_required
def click_msg_notice(request):
    """ Set db 'seen' field to 'True', and clean the number of message notice button. """

    result = {}
    user = request.user
    sender_list=[]
    sender_info_list=[]
    ## this loop get the whole msg sender's User object, the values is stored into a list
    for i in Event.objects.filter(user = user, content_type=mailinfo_type_object, seen=False):
        sender = i.event_object.mailtext.sender
        sender_list.append(sender)
        ## here, we change every item to seen         
        i.seen=True
        i.save()
    # via set() function, we can get a copy but without repeatable item 
    A = set(sender_list)
    # we ask every single item to get the detail info for every msg sender 
    for i in A:
        sender_info = {
                        "username":i.username,
                        "name":_show_obj_name(i.id),
                        "uid":i.id,
                        "avatar":settings.MEDIA_URL + str(Base.objects.get(user=i).imagesmall),
                        "count":sender_list.count(i),
        }
        sender_info_list.append(sender_info)

    print sender_info_list 
    result = {
            "senders":sender_info_list,
    }
    return result
