# -*- coding: utf8 -*-
from django import forms
from django.forms.extras.widgets import SelectDateWidget 
from iDenMail.models import MailText
from django.utils.translation import ugettext_lazy as _ 
# from captcha.fields import CaptchaField

class MailForm(forms.Form):

    content = forms.CharField(required = False,label=_(u"Summary"),max_length=200,widget=forms.Textarea)
    username = forms.CharField(label=_(u"username"),max_length=30,widget=forms.TextInput(attrs={'size': 20, 'class':'required'}))    