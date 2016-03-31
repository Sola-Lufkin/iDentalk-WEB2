# -*- coding: utf8 -*-
import re
from django import forms
from django.template.defaultfilters import mark_safe
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField
from django.contrib.auth.forms import PasswordChangeForm as auth_PWCForm

attrs_required = {'class': 'required'}
attrs_email = {'class': 'required', 'placeholder': 'Email'}
attrs_psw = {'class': 'required', 'placeholder': 'Password'}
required_tag = '<b class="required-tag">*</b>'

class LoginForm(forms.Form):
    username=forms.CharField(label=_("Email"),max_length=30,widget=forms.TextInput(attrs=attrs_email))
    password=forms.CharField(label=_("password"),max_length=30,widget=forms.PasswordInput(attrs=attrs_psw))

    def clean_pwd():
        self.cleaned_data['username'] = self.cleaned_data['username'].strip()

        if re.search(" ", self.cleaned_data['password']):
            raise forms.ValidationError(_("The password can not contain spaces."))
        else:
            return self.cleaned_data
    
class LoginAgainForm(forms.Form):
    username=forms.CharField(label=mark_safe(required_tag+"Email"),max_length=30,widget=forms.TextInput(attrs=attrs_required))
    password=forms.CharField(label=mark_safe(required_tag+"Password"),max_length=30,widget=forms.PasswordInput(attrs=attrs_required))
    captcha = CaptchaField()
    
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        self.cleaned_data['username'] = self.cleaned_data['username'].strip()
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])

        if not existing.exists():
            raise forms.ValidationError(_(u"User %s Not exist") % self.cleaned_data['username'])
        else:
            return self.cleaned_data['username']

    def clean_pwd():
        self.cleaned_data['username'] = self.cleaned_data['username'].strip()

        if re.search(" ", self.cleaned_data['password']):
            raise forms.ValidationError(_("The password can not contain spaces."))
        else:
            return self.cleaned_data

class PasswordChangeForm(auth_PWCForm):
    '''继承自django原生的PasswordChangeForm，此处从载了验证函数clean_new_password2'''
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        old_password = self.cleaned_data.get('old_password')

        if password1 and password2:
            if len(password1)<6:
                raise forms.ValidationError(_("The password fields need at least 6 characters."))

            else:
                if password1 != password2:
                    raise forms.ValidationError(_("The two password fields didn't match."))

                else:
                    if re.search(" ", password1):
                        # print 'password contain spaces'
                        # print re.search(" ", password1)
                        # print re.findall(" ", password1)
                        raise forms.ValidationError(_("The password can not contain spaces."))

                    else:
                        if old_password == password2:
                            raise forms.ValidationError(_("The new password should not same with the old one."))
                        else:
                            # print 'return le data'
                            # print self.cleaned_data
                            return self.cleaned_data
