# # -*- coding: utf-8 -*-
# import datetime
# from django.db import models
# from django.contrib import admin
# from django.contrib.auth.models import User
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes import generic
# from django.db.models.signals import post_save 
# from annoying.decorators import Signals 

# class PostTest(models.Model):
#     Tauthor = models.ForeignKey(User)
#     Ttitle = models.CharField(max_length=255)
#     Tcontent = models.TextField()
#     Tcreated = models.DateTimeField(u'发表时间', auto_now_add = True)
#     Tupdated = models.DateTimeField(u'最后修改时间', auto_now = True)
    
#     Tevents = generic.GenericRelation('Event')

#     def __unicode__(self):
#         return self.Ttitle
    
#     def description(self):
#         return u'%s %s 发表了日志《%s》' % (self.Tauthor.first_name, self.Tauthor.last_name, self.Ttitle)
    
# class PostTestAdmin(admin.ModelAdmin):
#     list_display = ('Tauthor','Ttitle','Tcontent','Tcreated','Tupdated','Tevents')

# admin.site.register(PostTest,PostTestAdmin)
    



# class Event(models.Model):
#     user = models.ForeignKey(User)
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.PositiveIntegerField()
    
#     event = generic.GenericForeignKey('content_type', 'object_id')
    
#     created = models.DateTimeField(u'事件发生时间', auto_now_add = True)
    
#     def __unicode__(self):
#         return  u"%s的事件: %s" % (self.user, self.description())
    
#     def description(self):
#         return self.event.description()
    
# class EventAdmin(admin.ModelAdmin):
#     list_display = ('user','content_type','object_id','event','created')

# admin.site.register(Event,EventAdmin)



# def post_post_save(sender, instance, signal, *args, **kwargs):
    
#     post = instance
#     print(post.description())
    
#     DATE_FORMAT = "%Y%m%d %H%M%S" 
#     created = post.Tcreated.strftime(DATE_FORMAT)
#     updated = post.Tcreated.strftime(DATE_FORMAT)
#     #此处系统将时间精确到0.000001，所以未经过处理的话，两个时间是不相等的
#     if created == updated:
# 	    event = Event(user=post.Tauthor,event = post)
# 	    event.save()

# post_save.connect(post_post_save, sender=PostTest)