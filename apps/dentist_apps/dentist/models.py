from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save
from notification.models import Event

# Question & Answer
class Qa(models.Model):
    
    #QA content
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=1000)
    place = models.IntegerField(null=True)
    #2User as the Foregin Key
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return (u'id: %s, question: %s, answer: %s') % (self.id, self.question, self.answer)
