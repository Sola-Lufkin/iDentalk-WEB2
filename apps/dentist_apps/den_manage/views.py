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
# from den_manage.models import *

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


# def _get_patlist_info(request,patient_type=""): # !!!leave for fuzhonghuan to check the patient_type var.
                                                  # found patient_type used in mydentalk show patient list.
def _get_patlist_info(request):	
	'''拉取病人列表'''
	
	template_var = {}
	RelationshipQuery = Relationship.objects.filter(dentist = request.user)

	# Connected_List = Relationship.objects.filter(dentist = request.user, status = 2)
	# Connecting_List = Relationship.objects.filter(dentist = request.user, status = 1)
	
	DATE_FORMAT = "%Y-%m-%d %H:%M"
	Follow_List = []
	Connected_List = []
	Connecting_List = []

	for i in RelationshipQuery:
		UserInfo = i.patient.user.user
		create_time = i.time.strftime(DATE_FORMAT)
		patient_id = UserInfo.id
		patient_name = _show_obj_name(object_id = patient_id)
		patient_avatar = i.patient.user.imagebig

		if i.status == 2:
			Connected_List.append({ 
				"patient_name":patient_name, 
				# "summary": patient
				"patient_id":patient_id, 
				"create_time":create_time,
				"avatar":settings.MEDIA_URL+str(patient_avatar),
				"mails_count":_latest_mails_count(request,patient_id),
			})
		elif i.status == 1:
			Connecting_List.append({
				"patient_name":patient_name, 
				"patient_id":patient_id, 
				"create_time":create_time,
				"avatar":settings.MEDIA_URL+str(patient_avatar),
		 	})
		elif i.status == 0:
			Follow_List.append({"patient_name":patient_name, 
								"patient_id":patient_id, 
								"create_time":create_time,
								"avatar":settings.MEDIA_URL+str(patient_avatar),
								})
			
	template_var = {
					"Follow_List":Follow_List,
					"follow_count":len(Follow_List),

					"Connected_List":Connected_List,
					"connected_count":len(Connected_List),
					
					"Connecting_List":Connecting_List,
					"connecting_count":len(Connecting_List),
	}

	# if patient_type=="" :
	# 	template_var = {
	# 					"Connected_List":Connected_List,
	# 					"connected_count":len(Connected_List),

	# 					"Connecting_List":Connecting_List,
	# 					"connecting_count":len(Connecting_List),
	# 	}
	# elif patient_type=="Connected" :
	# 	template_var = {
	# 				"Connected_List":Connected_List,
	# 				"connected_count":len(Connected_List),
	# 	}
	# elif patient_type=="Connecting" :
	# 	template_var = {
	# 					"Connecting_List":Connecting_List,
	# 					"connecting_count":len(Connecting_List),
	# 	}

	return template_var



def _relation_counts(request,dentistid="",patientid=""):
	''' 关系人数统计 '''

	status = -1
	if dentistid=="":
		RelationshipQuery = Relationship.objects.filter(dentist = request.user)
		
	else:
		Dentist = User.objects.get(id=dentistid)
		RelationshipQuery = Relationship.objects.filter(dentist = Dentist)
		try:
			Patient = User.objects.get(id=patientid)
			status = Relationship.objects.get(dentist = Dentist,patient = Patient).status
		except:
			pass

	follower_count=0
	patient_count=0
	for i in RelationshipQuery:

		if i.status == 0 or i.status == 1:
			follower_count = follower_count + 1
		elif i.status == 2:
			patient_count = patient_count + 1

	return {"follower_count":follower_count,
			"patient_count":patient_count,
			"status":status,
			}