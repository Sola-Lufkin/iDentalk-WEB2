# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save
#
from django.utils.translation import ugettext_lazy as _

class Event(models.Model):
    """Used to save post and comment change instance message"""
    # user is the notification sender or recevier?
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    event_object = generic.GenericForeignKey('content_type', 'object_id')

    # identity seen or not seen
    seen = models.BooleanField(_("seen"), default=False)
    archived = models.BooleanField(_("archived"), default=False)

    # connect request with message
    message = models.CharField(max_length=30, blank=True, null=True)
