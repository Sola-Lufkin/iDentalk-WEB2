#coding=utf-8
"""
Forms and validation code for user registration.

"""
import re
from django.contrib.auth.models import User
from django import forms
from django.template.defaultfilters import mark_safe
from django.utils.translation import ugettext_lazy as _


# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_required = {'class': 'required'}
attrs_email = {'class': 'required email'}
attrs_psw = {'minlength': '6', 'class': 'required'}
requireg_tag = "<b class='required-tag'>*</b>"

class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.
    
    """
    
    """ !!!!!!!!!!!!!!    此处为后期被注释掉，
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    """
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_email,
                                                               maxlength=75)),
                             label=_("Email"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_psw, render_value=False),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_psw, render_value=False),
                                label=_("Confirm"))
    # IDENTITY_CHOICES =(
    #     (u'D',_(u'Dentist')),
    #     (u'P',_(u'Patient')),
    #     )
    # identity = forms.ChoiceField(label=_('I am a'),choices=IDENTITY_CHOICES,
    #                              widget=forms.RadioSelect())    
    
    
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username'].strip()

    def clean_email(self):
        """
        Validate that the email is alphanumeric and is not already
        in use.
        
        """
        existing = User.objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that email already exists."))
        else:
            return self.cleaned_data['email'].strip()

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'email' in self.cleaned_data:
            self.cleaned_data['username'] = self.cleaned_data['email']

        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if len(self.cleaned_data['password1'])<6:
                raise forms.ValidationError(_("The password fields need at least 6 characters."))
            else:

                if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                    raise forms.ValidationError(_("The two password fields didn't match."))
                else:

                    if re.search(" ", self.cleaned_data['password1']):
                        # print 'password contain spaces'
                        # print re.search(" ", self.cleaned_data['password1'])
                        # print re.findall(" ", self.cleaned_data['password1'])
                        raise forms.ValidationError(_("The password can not contain spaces."))
                    else:
                        # print 'return le data'
                        # print self.cleaned_data
                        return self.cleaned_data

        # return self.cleaned_data
        #采用该方法实现 use the email as the username !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        


class RegistrationFormTermsOfService(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.
    
    """
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_required),
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={'required': _("You must agree to the terms to register")})


class RegistrationFormUniqueEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.
    
    """
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']

class ProfileForm(forms.Form):    
    first_name=forms.CharField(label=_(u"First Name"),max_length=30,widget=forms.TextInput(attrs={'size': 20,}))
    last_name=forms.CharField(label=_(u"Last Name"),max_length=30,widget=forms.TextInput(attrs={'size': 20,}))
    age=forms.CharField(label=_(u"Age"),max_length=30,widget=forms.TextInput(attrs={'size': 20,}))
    bio=forms.CharField(label=_(u"Bio"),max_length=30,widget=forms.TextInput(attrs={'size': 20,}))


class RegistrationFormNoFreeEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which disallows registration with
    email addresses from popular free webmail services; moderately
    useful for preventing automated spam registrations.
    
    To change the list of banned domains, subclass this form and
    override the attribute ``bad_domains``.
    
    """
    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com',
                   'yahoo.com']
    
    def clean_email(self):
        """
        Check the supplied email address against a list of known free
        webmail domains.
        
        """
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(_("Registration using free email addresses is prohibited. Please supply a different email address."))
        return self.cleaned_data['email']
