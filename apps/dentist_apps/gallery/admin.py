# -*- coding: utf8 -*-
from django.contrib import admin
from gallery.models import *

# Inline
class CaseInline(admin.StackedInline):
    model = Case
    
class CaseImgInline(admin.StackedInline):
    model = CaseImg

# ModelsAdmin
class CaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'dentistid',)
    inlines = [CaseImgInline,]
    
class CaseImgAdmin(admin.ModelAdmin):
    list_display = ('id', 'caseid',)

# Register
admin.site.register(Case, CaseAdmin)
admin.site.register(CaseImg, CaseImgAdmin)