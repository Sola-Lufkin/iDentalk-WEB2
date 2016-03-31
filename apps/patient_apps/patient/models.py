# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User
from profile.models import PatientProfile, DentistProfile
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save
from notification.models import Event
from utils import humantime

class Calendar(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    #identify patient add ownly or dentist add.
    color = models.CharField(max_length=10, default='blue')
    dentist_id = models.IntegerField(blank=True, null=True)
    patient = models.ForeignKey(PatientProfile)
    
    notice = generic.GenericRelation(Event)
    
    def __unicode__(self):
        return (u'Calendar ID %s. title %s. content %s. start %s. end %s') % (self.id, self.title, self.content, self.start, self.end)

    def calendar_desc(self):
        return (u'%s pcalendar_desc: "%s"') % (self.title, self.content)

def calendar_notice(sender, instance, **kwargs):
    patient_user = instance.patient.user.user
    event = Event(user=patient_user, event_object=instance)
    event.save()

post_save.connect(calendar_notice, sender=Calendar, dispatch_uid="my_unique_identifier")
