# -*- coding: utf8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save  #####
from django.utils.translation import ugettext_lazy as _ 
from iDentalk import settings
# Event Module
from notification.models import Event
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save

 
class MailText(models.Model):
    """docstring for MailText"""

    sender = models.ForeignKey(User)
    content = models.TextField(max_length=1000, blank=True, null=True)
    TYPE_TYPE = (
    		(0, _(u'Private')),
            (1, _(u'Public')),
            (2, _(u'Global')),
            (3,_(u'Calendar')),
    	)
    type = models.IntegerField(max_length=1,blank=False,choices=TYPE_TYPE)
    #group = 
    post_date = models.DateTimeField(auto_now_add=True)
    TYPE_STATUS =(
            (0, _(u'Unread')),
            (1, _(u'Read')),
            (2, _(u'Delete')),
            )      
    status = models.IntegerField(max_length=1,blank=False,choices=TYPE_STATUS, default=0) 

class MailTextAdmin(admin.ModelAdmin):
    list_display = ('sender','content','type','post_date','status')

admin.site.register(MailText,MailTextAdmin)

	
class MailInfo(models.Model):
    """docstring for MailInfo"""

    receiver = models.ForeignKey(User)
    TYPE_STATUS =(
            (0, _(u'Unread')),
            (1, _(u'Read')),
            (2, _(u'Delete')),
            )
    post_date = models.DateTimeField()        
    status = models.IntegerField(max_length=1,blank=False,choices=TYPE_STATUS, default = 0) 
    mailtext = models.ForeignKey(MailText)

    def msg_desc(self):
        msg_content = self.mailtext.content[0:15]
        return (u'%s, you have new message of "%s"') % (self.receiver.username, msg_content)

class MailInfoAdmin(admin.ModelAdmin):
    list_display = ('receiver','status')

admin.site.register(MailInfo,MailInfoAdmin)


def event_save(sender, instance, **kwargs):
    receive_user = instance.receiver
    print(receive_user)

    if instance.status == 0:
        event = Event(user=receive_user, event_object=instance)
        event.save()

    else:
        pass

post_save.connect(event_save, sender=MailInfo, dispatch_uid="my_unique_identifier")
