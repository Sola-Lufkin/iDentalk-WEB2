# -*- coding: utf8 -*-
from relationship.models import *
from django.contrib import admin

##ModelsAdmins
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('patient','dentist','status','time')
        

##Register
admin.site.register(Relationship,RelationshipAdmin)

