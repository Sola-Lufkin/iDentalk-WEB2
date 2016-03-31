# -*- coding: utf8 -*-
from profile.models import *
from django.contrib import admin
from gallery.admin import * # (Update fuwh)

##Inlines
class WorkPlaceInline(admin.StackedInline):
    model = WorkPlace
    

class DentistProfileInline(admin.StackedInline):
    model = DentistProfile 

class TagListInline(admin.StackedInline):
    model = TagList
    
    

##ModelsAdmins
class BaseAdmin(admin.ModelAdmin):
    list_display = ('user','identity',)
        

class DentistProfileAdmin(admin.ModelAdmin):
    list_display = ('user','prove_verify',)
    inlines = [TagListInline,WorkPlaceInline,CaseInline,]

class TagAdmin(admin.ModelAdmin):
    list_display = ('id','name','tagtype','verify',)

class WorkPlaceAdmin(admin.ModelAdmin):
    list_display = ('id','dentistid','location',)
    
class TagListAdmin(admin.ModelAdmin):
    list_display = ('id','dentistid','tagid','tagtype',)

class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

##Register
admin.site.register(Base,BaseAdmin)
admin.site.register(DentistProfile,DentistProfileAdmin)
admin.site.register(PatientProfile,PatientProfileAdmin)
admin.site.register(WorkPlace,WorkPlaceAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(TagList,TagListAdmin)
