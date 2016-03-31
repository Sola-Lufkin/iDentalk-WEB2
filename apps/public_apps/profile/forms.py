# -*- coding: utf8 -*-
from django import forms
from django.template.defaultfilters import mark_safe
from django.forms.extras.widgets import SelectDateWidget 
from profile.models import Base, DentistProfile, PatientProfile
from django.utils.translation import ugettext_lazy as _ 
from captcha.fields import CaptchaField

#病人第一次注册填写的信息表单
requireg_tag = "<b class='required-tag'>*</b>"
class PatientStep1(forms.Form):
    
    first_name = forms.CharField(label=mark_safe(requireg_tag+"First name"),max_length=30,widget=forms.TextInput(attrs={'size': 20,'class':'required'}))
    last_name = forms.CharField(label=mark_safe(requireg_tag+"Last name"),max_length=30,widget=forms.TextInput(attrs={'size': 20,'class':'required'}))
    TITLE_CHOICES =(
    (u'1',_(u'Mr.')),
    (u'2',_(u'Mrs.')),
    (u'3',_(u'Ms.')),
    )
    title = forms.ChoiceField(label=mark_safe(requireg_tag+'Your title'),choices=TITLE_CHOICES,widget=forms.RadioSelect(attrs={'class':'required'}))           

#医生第一次注册填写的信息表单
class DentistStep1(forms.Form): 

    first_name = forms.CharField(label=mark_safe(requireg_tag+"First name"),max_length=30,widget=forms.TextInput(attrs={'size': 20,'class':'required'}))
    last_name = forms.CharField(label=mark_safe(requireg_tag+"Last name"),max_length=30,widget=forms.TextInput(attrs={'size': 20, 'class':'required'}))    
    TITLE_CHOICES =(
    (u'1',_(u'Dr.')),
    (u'2',_(u'Prof.')),
    (u'3',_(u'Mr.')),
    (u'4',_(u'Ms.')),
    (u'5',_(u'Dr(Prof).')),
    )
    title = forms.ChoiceField(label=mark_safe(requireg_tag+'Your title'),choices=TITLE_CHOICES,widget=forms.RadioSelect(attrs={'class':'required'}))           
    ##captcha = CaptchaField()#####验证码

#图片表单
class ImgForm(forms.Form): 
    
    imagephoto = forms.ImageField(required = False,label=_(u'Upload your img')) 

#证明图表单
class VerPicForm(forms.Form): 
    
    prove_pic = forms.ImageField(required = False,label=_(u'Upload your verify img')) 


#医生的基本信息表单
class DentistProfileBaseForm(forms.Form):
    
    first_name = forms.CharField(label=_(u"First name"),max_length=30,widget=forms.TextInput(attrs={'size': 20,}))
    middle_name = forms.CharField(label=_(u"Middle name"),required = False,max_length=30,widget=forms.TextInput(attrs={'size': 20,}))
    last_name = forms.CharField(label=_(u"Last name"),max_length=30,widget=forms.TextInput(attrs={'size': 20,}))
    show_mid_name = forms.BooleanField(label=_(u"Show my Middle name"),required = False)
    TITLE_CHOICES =(
    (u'1',_(u'Dr.')),
    (u'2',_(u'Prof.')),
    (u'3',_(u'Mr.')),
    (u'4',_(u'Ms.')),
    (u'5',_(u'Dr(Prof).')),
    )
    title = forms.ChoiceField(label=_(u'My title'),choices=TITLE_CHOICES,widget=forms.RadioSelect()) 
    workemail = forms.EmailField(label=_(u'Work Email'),required = False,max_length=75,widget=forms.TextInput(attrs={'size': 20,}))
    
       
    
#医生的地址信息表单
class DentistProfileLocForm(forms.Form):
    
    clinic_name = forms.CharField(label=_(u"Clinic name"),max_length=100,widget=forms.TextInput(attrs={'size':20,'class':'required'}))
    location = forms.CharField(label=_(u"Clinic location"),max_length=200,widget=forms.TextInput(attrs={'size':20,'class':'required'}))
    # latitude = forms.CharField(required = False)
    postcode = forms.CharField(required = False,label=_(u"Post code"),max_length=10,widget=forms.TextInput(attrs={'size':20,}))
    tel = forms.CharField(required = False,label=_(u"Tel"),max_length=30,widget=forms.TextInput(attrs={'size':20,}))
    business_hours_start = forms.TimeField(required = False,label=_(u"Start"),widget=forms.TextInput(attrs={'class':'timepicker'}))
    business_hours_end = forms.TimeField(required = False,label=_(u"To"),widget=forms.TextInput(attrs={'class':'timepicker'}))

#医生的个人简述表单
class DentistProfileSumForm(forms.Form):
    
    summary = forms.CharField(required = False,label=_(u"Summary"),max_length=200,widget=forms.Textarea)
    
#医生的Feild表单
class DentistProfileFeildForm(forms.Form):
    
    Tag_CHOICES =(
        ('Cosmetic dentistry', 'Cosmetic dentistry' ),
        ('Dental anesthesiology', 'Dental anesthesiology' ),
        ( 'Dental hygienist', 'Dental hygienist' ),
        ( 'Dental public health', 'Dental public health' ),
        ( 'Endodontics', 'Endodontics' ),
        ( 'Family dentistry', 'Family dentistry' ),
        ( 'General dentistry', 'General dentistry' ),
        ( 'Geriatric dentistry', 'Geriatric dentistry' ),
        ( 'Oral and maxillofacial pathology', 'Oral and maxillofacial pathology' ),
        ( 'Oral and maxillofacial radiology', 'Oral and maxillofacial radiology' ),
        ( 'Oral and maxillofacial surgery', 'Oral and maxillofacial surgery' ),
        ( 'Oral medicine', 'Oral medicine' ),
        ( 'Orthodontics', 'Orthodontics' ),
        ( 'Pediatric dentistry', 'Pediatric dentistry' ),
        ( 'Periodontics', 'Periodontics' ),
        ( 'Prosthodontics', 'Prosthodontics' ),
        )    
        
    #Tag  = forms.CharField(label=_(u"标签"),max_length=400,widget=forms.TextInput(attrs={'size':60,}))
    Tag = forms.ChoiceField(choices=Tag_CHOICES,required = False, widget=forms.Select(attrs={'class': 'chzn-select','data-placeholder':'Choose Your Fields...','multiple style':'width:350px;','tabindex':'4','multiple':'multiple'})) 

#医生的Degree表单    
class DentistProfileDegreeForm(forms.Form):
        
    Tag_CHOICES =(
        ('Bachelor of Dental Science (BDSc)', 'Bachelor of Dental Science (BDSc)' ),
        ('Bachelor of Dental Surgery (BDS)', 'Bachelor of Dental Surgery (BDS)' ),
        ( 'Bachelor of Dentistry (BDent)', 'Bachelor of Dentistry (BDent)' ),
        ( 'Bachelor of Oral Health in Dental Science (B OH DS', 'Bachelor of Oral Health in Dental Science (B OH DS' ),
        ( 'Graduate Diploma in Dentistry (Grad Dip Dent)', 'Graduate Diploma in Dentistry (Grad Dip Dent)' ),
        ( 'Master of Dental Science (MDSc)', 'Master of Dental Science (MDSc)' ),
        ( 'Master of Dental Surgery (MDS)', 'Master of Dental Surgery (MDS)' ),
        ( 'Master of Dentistry (MDent)', 'Master of Dentistry (MDent)' ),
        ( 'Master of Medical Science (MMSc)', 'Master of Medical Science (MMSc)' ),
        ( 'Master of Science (MSc)', 'Master of Science (MSc)' ),
        ( 'Doctor of Clinical Dentistry (DClinDent)', 'Doctor of Clinical Dentistry (DClinDent)' ),
        ( 'Doctor of Dental Medicine (DMD)', 'Doctor of Dental Medicine (DMD)' ),
        ( 'Doctor of Dental Science (DDSc)', 'Doctor of Dental Science (DDSc)' ),
        ( 'Doctor of Dental Surgery (DDS)', 'Doctor of Dental Surgery (DDS)' ),
        ( 'Doctor of Medical Dentistry (DrMedDent)', 'Doctor of Medical Dentistry (DrMedDent)' ),
        ( 'Doctor of Medical Science (DMSc)', 'Doctor of Medical Science (DMSc)' ),
        ( 'Doctor of Philosophy (PhD)', 'Doctor of Philosophy (PhD)' ),
        )    
            
    #Tag  = forms.CharField(label=_(u"标签"),max_length=400,widget=forms.TextInput(attrs={'size':60,}))
    Tag = forms.ChoiceField(choices=Tag_CHOICES,required = False, widget=forms.Select(attrs={'class': 'chzn-select','data-placeholder':'Choose Your Fields...','multiple style':'width:350px;','tabindex':'4','multiple':'multiple'}))     


#病人的个人简述表单
class PatientProfileSumForm(forms.Form):
    
    summary = forms.CharField(required = False,label=_(u"Summary"),max_length=200,widget=forms.Textarea)
#病人的基本信息表单
class PatientProfileBaseForm(forms.Form):
    
    first_name = forms.CharField(label=_(u"First name"),max_length=30,widget=forms.TextInput(attrs={'size': 20,}))
    middle_name = forms.CharField(label=_(u"Middle name"),required = False,max_length=30,widget=forms.TextInput(attrs={'size': 20,}))
    last_name = forms.CharField(label=_(u"Last name"),max_length=30,widget=forms.TextInput(attrs={'size': 20,}))
    GENDER_CHOICES =(
    (u'M',_(u'Male')),
    (u'F',_(u'Female')),
    )
    gender = forms.ChoiceField(required = False,label=_(u'Gender'),choices=GENDER_CHOICES,widget=forms.RadioSelect())
    ##birthday = forms.DateField(widget=extras.SelectDateWidget)
    birthday = forms.DateField(required = False)
    workemail = forms.EmailField(label=_(u'Email'),required = False,max_length=75,widget=forms.TextInput(attrs={'size': 20,}))
    location = forms.CharField(required = False,label=_(u'Location'),max_length=200,widget=forms.TextInput(attrs={'size':20,}))
    latitude = forms.FloatField(required = False)
    longitude = forms.FloatField(required = False)            
    