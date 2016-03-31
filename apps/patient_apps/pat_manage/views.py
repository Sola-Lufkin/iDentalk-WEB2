# Create your views here.
# -*- coding: utf8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User   
from django.utils.translation import ugettext_lazy as _ 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from iDentalk import settings
from relationship.models import Relationship
from profile.models import Base
from public.views import _show_obj_name
from iDentalk.decorators import require_identity_type
from iDenMail.models import MailInfo

from annoying.decorators import render_to, ajax_request
from utils import JsonResponse, json_serialize
from django.utils import simplejson as json


def _latest_mails_count(request,object_id):

    UserObj =User.objects.get(username=request.user)
    contacter = User.objects.get(id=object_id)
    count = 0
    for i in [entry.mailtext for entry in MailInfo.objects.filter(receiver = UserObj,status='0')]:
        if i.sender == contacter:
            count = count + 1
    print("未读消息:%s"%count)
    return count



def _get_denlist_info(request):	
	'''拉取医生列表'''
	
	template_var = {}
	RelationshipQuery = Relationship.objects.filter(patient = request.user)

	# Follow_List = Relationship.objects.filter(patient = request.user, status = 0)
	# Connected_List = Relationship.objects.filter(patient = request.user, status = 2)
	# Connecting_List = Relationship.objects.filter(patient = request.user, status = 1)

	DATE_FORMAT = "%Y-%m-%d %H:%M"
	Follow_List = []
	Connected_List = []
	Connecting_List = []
	for i in RelationshipQuery:
		UserInfo = i.dentist.user.user
		create_time = i.time.strftime(DATE_FORMAT)
		dentist_id = UserInfo.id
		dentist_name = _show_obj_name(object_id = dentist_id)
		dentist_avatar = i.dentist.user.imagebig

		if i.status == 2:		
			Connected_List.append({ "dentist_name":dentist_name, 
								    "dentist_id":dentist_id, 
								    "create_time":create_time,
								    "avatar": settings.MEDIA_URL+str(dentist_avatar),
								    "mails_count":_latest_mails_count(request,dentist_id),
								 })
		elif i.status == 1:
			Connecting_List.append({"dentist_name":dentist_name, 
									"dentist_id":dentist_id, 
									"create_time":create_time,
									"avatar":settings.MEDIA_URL+str(dentist_avatar),
								 })
		elif i.status == 0:
			Follow_List.append({"dentist_name":dentist_name,
								"dentist_id":dentist_id,
								"create_time":create_time,
								"avatar":settings.MEDIA_URL+str(dentist_avatar),

							   	})

	template_var = {
					"Follow_List":Follow_List,
					"follow_count":len(Follow_List),

					"Connected_List":Connected_List,
					"connected_count":len(Connected_List),
					
					"Connecting_List":Connecting_List,
					"connecting_count":len(Connecting_List),
	}

	return template_var


# @render_to("patient/patient_denlist.html")
# @require_identity_type("Patient")
# # @ajax_request
# def denlist(request):
#     '''病人列表页面'''

#     template_var = _get_denlist_info(request)
#     return template_var