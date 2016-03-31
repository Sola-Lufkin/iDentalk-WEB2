# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from profile.models import DentistProfile
from iDentalk import settings

# 医生Case Gallery
class Case(models.Model):
    
    #1Case Description
    case_name = models.CharField(max_length=40, blank=False, null=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    img_count = models.IntegerField(default=0)
    #2DentistProfile as the Foregin Key
    dentistid = models.ForeignKey(DentistProfile)
    
    def __unicode__(self):
        return (u'Case编号%s. [由"%s"创建]') % (self.id, self.dentistid)
    
# 医生Case Image
class CaseImg(models.Model):
    
    #1Case Image
    bef_img = models.ImageField(upload_to="uploaded/", blank=False)
    aft_img = models.ImageField(upload_to="uploaded/", blank=False)
    #2Case as the Foreign Key
    caseid = models.ForeignKey(Case)
    
    def __unicode__(self):
        return (u'%s.%s') % (self.id, self.caseid)
