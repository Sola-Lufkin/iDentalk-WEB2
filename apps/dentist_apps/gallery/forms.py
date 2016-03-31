# -*- coding: utf8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _ 

# 病例描述
class CaseDescForm(forms.Form):
    description = forms.CharField(required=True, label=_(u"描述"), max_length=300, widget=forms.Textarea)

# 病例图片
class CaseImgForm(forms.Form):
    bef_img = forms.ImageField(required=False, label="Before Image")
    aft_img = forms.ImageField(required=False, label="After Image")
