# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save
from notification.models import Event
from public.views import _show_obj_name
from utils import humantime

# New things Post
class Post(models.Model):
    
    #1Post content
    post_content = models.TextField(null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to="uploaded/",null=True)
    img_s = models.ImageField(upload_to="uploaded/", null=True)
    img_m = models.ImageField(upload_to="uploaded/", null=True)
    url = models.URLField(max_length=300, null=True)
    comment_count = models.IntegerField()
    #2User as the Foregin Key
    user_id = models.ForeignKey(User)
    events = generic.GenericRelation(Event)
    
    def __unicode__(self):
        return (u'Post编号%s. [由"%s"发布]') % (self.id, self.user_id)

    def post_desc(self):
        return (u'%s post a new info: "%s"') % (self.user_id, self.post_content)
    
# Comments for new things Post
class Comment(models.Model):
    
    #1Comment content
    comment_content = models.TextField(null=True)
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_author_ip = models.IPAddressField()

    #2User&Post  as the Foreign Key
    user_id = models.ForeignKey(User)
    post_id = models.ForeignKey(Post)
    events = generic.GenericRelation(Event)
    
    def __unicode__(self):
        return (u'Comment编号%s.Post编号%s.%s') % (self.id, self.post_id, self.user_id)

    def comment_desc(self):
        pid = self.post_id.id
        post_content = self.post_id.post_content
        post_piece = post_content[0:15]
        # print(post_piece)
        name = _show_obj_name(self.user_id.id)
        # print 0
        comment_date_show = humantime(self.comment_date)
        # print comment_date_show
        # print 11

        return (u' %s, %s commented on your post "%s"') % ( comment_date_show, name, post_piece)

def post_event_put(sender, instance, **kwargs):
    """sender是信号发送者（Model），instance是其实例"""

    post_type_object = ContentType.objects.get(model='post')

    if Event.objects.filter(user=instance.user_id, content_type=post_type_object, object_id=instance.id).exists():
        pass  # for prevent modify post comment_count update save again when delete comment
    else:
        event = Event(user=instance.user_id, event_object=instance)
        event.save()

def comment_event_put(sender, instance, **kwargs):
    """sender是信号发送者（Model），instance是其实例"""

    if instance.user_id != instance.post_id.user_id:  # for prevent record user comment in himself post
        event = Event(user=instance.user_id, event_object=instance)
        event.save()
    else:
        pass

post_save.connect(post_event_put, sender=Post, dispatch_uid="my_unique_identifier")  # 添加dispatch_uid保证每次事件只会被记录一次
post_save.connect(comment_event_put, sender=Comment, dispatch_uid="my_unique_identifier")  # connect action on Comment & Event
