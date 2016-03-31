# -*- coding: utf8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils import simplejson as json

from annoying.decorators import render_to, ajax_request
from profile.models import Base, DentistProfile, PatientProfile
from django.contrib.contenttypes.models import ContentType
from relationship.models import Relationship
from notification.models import Event


@csrf_exempt
@require_http_methods(["POST"])
@ajax_request
@login_required
def follow(request,object_id):
    '''用户（身份病人）follow'''

    result = {} 
    dentistuser = User.objects.get(id=object_id)
    DentistProfileObj = DentistProfile.objects.get(user=dentistuser)
    PatientProfileObj = PatientProfile.objects.get(user=request.user)
    
    try:
        Relationship.objects.get(patient = PatientProfileObj,dentist = DentistProfileObj)
        result = {
                "msg":"Failure",
                "status":0,
        }


    except:

        RelationshipNew = Relationship(patient = PatientProfileObj,dentist = DentistProfileObj,status = 0)
        RelationshipNew.save()
        result = {
                "msg":"Success",
                "status":1,
        }
    
    return result


@csrf_exempt
@require_http_methods(["POST"])
@ajax_request
@login_required
def unfollow(request,object_id):
    '''用户（身份病人）unfollow'''
    
    result = {}
    dentistuser = User.objects.get(id=object_id)
    
    DentistProfileObj = DentistProfile.objects.get(user=dentistuser)
    PatientProfileObj = PatientProfile.objects.get(user=request.user)        
    
    try:
        Relationship.objects.get(patient = PatientProfileObj,dentist = DentistProfileObj).delete()

        result = {
                "msg":"Success",
                "status":1,
        }

    except:
        result = {
                "msg":"Failure",
                "status":0,
        }

    return result


@csrf_exempt
@require_http_methods(["POST"])
@ajax_request
@login_required
def connect(request,object_id):
    '''用户（身份病人）发送connect请求'''
    
    result = {}

    data = json.loads(request.POST['data'])
    msg = data['msg']
    msg = msg.strip()

    receiver = User.objects.filter(id=object_id)
    dentistuser = receiver[0]
    patient = request.user
    DentistProfileObj = DentistProfile.objects.get(user=dentistuser)
    PatientProfileObj = PatientProfile.objects.get(user=request.user)
       
    try:
        RelationshipObj = Relationship.objects.get(patient = PatientProfileObj,dentist = DentistProfileObj)

        if RelationshipObj.status == 0:

            RelationshipObj.status=1
            RelationshipObj.save()

            relation_type_object = ContentType.objects.get(model='relationship')
            Event.objects.filter(user=patient, content_type=relation_type_object, object_id=RelationshipObj.id).update(message=msg)

        result = {
                    "msg":"Success",
                    "status":1,
        }

    except:

        RelationshipNew = Relationship(patient = PatientProfileObj,dentist = DentistProfileObj,status = 1)
        RelationshipNew.save()

        relation_type_object = ContentType.objects.get(model='relationship')
        Event.objects.filter(user=patient, content_type=relation_type_object, object_id=RelationshipNew.id).update(message=msg)

        result = {
                    "msg":"Success",
                    "status":1,
        }

    return result


@csrf_exempt
@require_http_methods(["POST"])
@ajax_request
@login_required
def connecting_cancel(request,object_id):
    '''patient refuse connect request'''
    
    result = {}
    dentistuser = User.objects.get(id=object_id)
    patient = request.user

    DentistProfileObj = DentistProfile.objects.get(user=dentistuser)
    PatientProfileObj = PatientProfile.objects.get(user=request.user)
               
    try:
        RelationshipObj = Relationship.objects.get(patient = PatientProfileObj,dentist = DentistProfileObj)

        if RelationshipObj.status == 1:

            RelationshipObj.status=0
            RelationshipObj.save()

            ''' for prevent from recording status changed to =0, delete event when status changed to 0 '''
            relation_type_object = ContentType.objects.get(model='relationship')
            Event.objects.get(user=patient, content_type=relation_type_object, object_id=RelationshipObj.id).delete()

        result = {
                "msg":"Success",
                "status":1,
        }

    except:
        result = {
                "msg":"Failure",
                "status":0,
        }

    return result


@csrf_exempt
@require_http_methods(["POST"])
@ajax_request
@login_required
def refuse_request(request,object_id):
    '''dentist refuse connect request'''
    
    result = {}
    patient = User.objects.get(id=object_id)
    DentistProfileObj = DentistProfile.objects.get(user=request.user)
    PatientProfileObj = PatientProfile.objects.get(user=patient)

    try:
        RelationshipObj = Relationship.objects.get(patient = PatientProfileObj,dentist = DentistProfileObj)


        if RelationshipObj.status == 1:

            RelationshipObj.status=0
            RelationshipObj.save()
 
            # relation_type_object = ContentType.objects.get(model='relationship')
            # Event.objects.filter(user=patient, content_type=relation_type_object, object_id=RelationshipObj.id, archived=False).update(archived=True)

            ''' for prevent from recording status changed to =0, delete event when status changed to 0 '''
            relation_type_object = ContentType.objects.get(model='relationship')
            Event.objects.get(user=patient, content_type=relation_type_object, object_id=RelationshipObj.id).delete()

        result = {
                "msg":"Success",
                "status":1,
        }

    except:
        result = {
                "msg":"Failure",
                "status":0,
        }
        
    return result


@csrf_exempt
@require_http_methods(["POST"])
@ajax_request
@login_required
def accept_request(request,object_id):
    '''用户（身份医生）确认connect请求'''
    
    result = {}
    receiver = User.objects.filter(id=object_id)
    patient = User.objects.get(id=object_id)
    DentistProfileObj = DentistProfile.objects.get(user=request.user)
    PatientProfileObj = PatientProfile.objects.get(user=patient)

    try:
        RelationshipObj = Relationship.objects.get(patient = PatientProfileObj,dentist = DentistProfileObj)


        if RelationshipObj.status == 1:

            RelationshipObj.status=2
            RelationshipObj.save()
            # Next! Relation model changed status = 2, will make Event put a new relation notice record, send from dentist user.

            # Then update patient sent relation notice's archieve=True, there will be 2 notice point to relation, Obj.id.
            relation_type_object = ContentType.objects.get(model='relationship')
            Event.objects.filter(user=patient, content_type=relation_type_object, object_id=RelationshipObj.id, archived=False).update(archived=True)

        result = {
                "msg":"Success",
                "status":1,
        }

    except:
        result = {
                "msg":"Failure",
                "status":0,
        }

    return result


@csrf_exempt
@require_http_methods(["POST"])
@ajax_request
@login_required
def unconnect(request,object_id):
    '''用户unconnect'''
    
    result = {}
    try:
        dentist = User.objects.get(id=object_id)
        patient = request.user
        DentistProfileObj = DentistProfile.objects.get(user=dentist)
        PatientProfileObj = PatientProfile.objects.get(user=patient)

    except:
        dentist = request.user
        patient = User.objects.get(id=object_id)
        DentistProfileObj = DentistProfile.objects.get(user=dentist)
        PatientProfileObj = PatientProfile.objects.get(user=patient)
                
    try:
        RelationshipObj = Relationship.objects.get(patient = PatientProfileObj,dentist = DentistProfileObj)

        if RelationshipObj.status == 2:

            RelationshipObj.status=0
            RelationshipObj.save()

            ''' delete 2 times notice where they connectting&connected before, but now they follow status changed to 0 '''
            relation_type_object = ContentType.objects.get(model='relationship')
            Event.objects.get(user=patient, content_type=relation_type_object, object_id=RelationshipObj.id).delete()
            Event.objects.get(user=dentist, content_type=relation_type_object, object_id=RelationshipObj.id).delete()

        result = {
                "msg":"Success",
                "status":1,
        }

    except:
        result = {
                "msg":"Failure",
                "status":0,
        }
        
    return result
