# coding=utf-8
from django.contrib import admin
from notification.models import *

class EventAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'seen', 'archived')


admin.site.register(Event, EventAdmin)
