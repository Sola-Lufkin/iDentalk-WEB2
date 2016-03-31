# -*- coding: utf8 -*-
from django.db import models
from profile.models import PatientProfile, DentistProfile 
from django.utils.translation import ugettext_lazy as _ 
# Event Module
from notification.models import Event
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save
from public.views import _show_obj_name
from profile.models import Base
from iDentalk import settings

class Relationship(models.Model):
    
    patient = models.ForeignKey(PatientProfile)
    dentist = models.ForeignKey(DentistProfile)
    
    STATUS_CHOICES =(
            (0, _(u'关注但未连接')),
            (1, _(u'申请连接中（默认关注）')),
            (2, _(u'已经连接（默认关注）')),
            )    
    status = models.IntegerField(max_length=1,blank=False,choices=STATUS_CHOICES) 
    time = models.DateTimeField('关系创建时间',auto_now_add = True)

    #2 reverse mapping Event Table
    events = generic.GenericRelation(Event)

    def relation_connecting_desc(self):
        return (u'%s wants to connect with you.') % (_show_obj_name(self.patient.user.user.id) )

    def pget_imagesamll(self):
        BaseObj = Base.objects.get(user=self.patient)
        print "Get Small Image"
        print settings.MEDIA_URL
        print BaseObj.imagesmall
        return settings.MEDIA_URL + str(BaseObj.imagesmall)

    def dget_imagesamll(self):
        BaseObj = Base.objects.get(user=self.dentist)
        return settings.MEDIA_URL + str(BaseObj.imagesmall)

    def relation_connected_desc(self):
    	return (u'%s has connected to you.') % (_show_obj_name(self.dentist.user.user.id) )

def request_event_put(sender, instance, **kwargs):
    dentist_user = instance.dentist.user.user
    patient_user = instance.patient.user.user

    if instance.status == 1:  # only listen relationship status=1 signal just mean: Patient request to Connect Dentist
        event = Event(user=patient_user, event_object=instance)
        event.save()

    elif instance.status == 2:  # only listen relationship status=2 signal just mean: Dentist accept Patient Connect
        event = Event(user=dentist_user, event_object=instance)
        event.save()

    else:
        pass

post_save.connect(request_event_put, sender=Relationship, dispatch_uid="my_unique_identifier")
