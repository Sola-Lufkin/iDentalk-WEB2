# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save  #####
from django.utils.translation import ugettext_lazy as _ 
from iDentalk import settings
 
#基本的Profile信息 
class Base(models.Model):
    
    #1)与User一对一的主键
    user = models.OneToOneField(User, primary_key = True,unique=True)
    #2)用户身份
    IDENTITY_CHOICES =(
    (u'D',_(u'牙科医生')),
    (u'P',_(u'患者')),
    )
    identity = models.CharField(max_length=1,choices=IDENTITY_CHOICES)
    #3)中间名
    middle_name = models.CharField(max_length=30,blank=True,null=True)
    #4)头像
    imagephoto = models.ImageField(upload_to="uploadImages/",blank=True,null=True,default="site_static/img/8.png") #这样的upload_to有问题
    imagebig = models.ImageField(upload_to="uploadImages/",blank=True,null=True,default="site_static/img/head_250_250.png")   # 
    imagesmall = models.ImageField(upload_to="uploadImages/",blank=True,null=True,default="site_static/img/head_50_50.png") #
    pic_ext = models.CharField(max_length=10,blank=True,null=True)
    #5)用户性别
    GENDER_CHOICES =(
    (u'M',_(u'Male')),
    (u'F',_(u'Female')),
    )
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,blank=True)
    #6)生日
    birthday = models.DateField(max_length=20,blank=True,null=True)
    #7)用户自我描述
    summary = models.TextField(max_length=200,blank=True,null=True,default="")
    #8)工作 Email
    workemail = models.EmailField(max_length=75,blank=True,null=True,default="")
    #9)完成身份选择的标识
    #finish_idchoice = models.BooleanField(default = False )    ####此字段可以删除掉，而换用identity字段是否为空来判断
    #10)完成注册信息填写的标识
    finish_steps = models.BooleanField(default = False )
    #11)显示中间名
    show_mid_name = models.BooleanField(default = False )
    same_account_email = models.BooleanField(default = False )
    
    def __unicode__(self):
        return u'%s | %s %s | %s' % (self.user, self.user.first_name, self.user.last_name, self.identity)
    
    
# Register a handler for the User model's django.db.models.signals.post_save signal and, 
# in the handler, if created is True, create the associated user profile: 注，该函数在User表单提交时自动执行
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        #UserProfile.objects.create(user=instance)
        Base.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

#病人Profile    
class PatientProfile(models.Model):
    
    #1)USER
    user = models.OneToOneField(Base, primary_key = True,unique=True)
    #2)Title
    TITLE_CHOICES =(
    (u'1',_(u'Mr.')),
    (u'2',_(u'Miss.')),
    (u'3',_(u'Ms.')),
    (u'4',_(u'Mrs.')),
    )
    title = models.CharField(max_length=1,choices=TITLE_CHOICES,blank=True)
    #3)地理位置 
    location = models.CharField(max_length = 200,blank=True,null=True,default="")
    latitude = models.DecimalField(blank=True,null=True,max_digits=13, decimal_places=10)
    longitude = models.DecimalField(blank=True,null=True,max_digits=13, decimal_places=10)
    #4)病理信息
    medical_history = models.CharField(max_length = 200,blank =True,null=True)
    treatment_history = models.CharField(max_length = 200,blank =True,null=True)
    oral_habit = models.CharField(max_length = 200,blank =True,null=True)
    oral_status = models.CharField(max_length = 200,blank =True,null=True)
    
    def __unicode__(self):
        return (u'%s') % (self.user)


#医生Profile
class DentistProfile(models.Model):
    
    #1)USER
    user = models.OneToOneField(Base, primary_key = True,unique=True) 
    #2)Title
    TITLE_CHOICES =(
    (u'1',_(u'Dr.')),
    (u'2',_(u'Prof.')),
    (u'3',_(u'Mr.')),
    (u'4',_(u'Ms.')),
    (u'5',_(u'Dr(Prof).')),
    )    
    title = models.CharField(max_length=1,choices=TITLE_CHOICES,default='1')
    #3)WebSNS
    website = models.CharField(max_length=50,blank=True,null=True)
    twitter = models.CharField(max_length=50,blank=True,null=True)
    facebook = models.CharField(max_length=50,blank=True,null=True)
    #4)Prove Picture
    prove_pic = models.ImageField(upload_to="uploaded/",blank=True,null=True)
    #5)Flag of Prove
    VERIFY_CHOICES =(
    (u'Y',_(u'已经通过验证')),
    (u'N',_(u'用户还没有提交验证图片')),
    (u'S',_(u'图片正在人工验证中')),
    )
    prove_verify = models.CharField(max_length=1,choices=VERIFY_CHOICES,default='N')
    #6)Flag of push 
    pushed = models.BooleanField(default = True ) 
    #7)Count
    workplace_count = models.IntegerField(default=0)
    case_count = models.IntegerField(default=0)
    degree_count = models.IntegerField(default=0)
    feild_count = models.IntegerField(default=0) 
    
    def __unicode__(self):
        return (u'%s') % (self.user)    


#医生WorkPlace
class WorkPlace(models.Model):
    
    #1)Location Info
    clinic_name = models.CharField(max_length = 100,blank=True,null=True)
    location = models.CharField(max_length = 200,blank=True,null=True)

    ###################
    latitude = models.DecimalField(blank=True,null=True,max_digits=13, decimal_places=10)
    longitude = models.DecimalField(blank=True,null=True,max_digits=13, decimal_places=10)
    #2)PostCode
    postcode = models.CharField(max_length=10,blank=True,null=True)
    #3)Tel
    tel = models.CharField(max_length=30,blank=True,null=True)
    #4)Business Hours
    business_hour = models.TextField(max_length=200,blank=True,null=True)
    #5)DentistProfile as the ForeignKey
    dentistid = models.ForeignKey(DentistProfile)
    
    def __unicode__(self):
        return (u'用户:%s.地址:%s ') % (self.dentistid,self.location)    
  

#Tag库
class Tag(models.Model):
        
    #1)Tag Name
    name = models.CharField(max_length=50,blank=False,default="unnamed")
    #2)Tag Verify
    verify = models.BooleanField(blank=False)
    #3)Tag Type
    TYPE_CHOICES =(
            (u'F',_(u'Feild')),
            (u'D',_(u'Degree')),
            )       
    tagtype = models.CharField(max_length=1,blank=False,choices=TYPE_CHOICES) 
       
    #def __unicode__(self):
        #return (u'No.%s %s Type:%s') % (self.id,self.name,self.tagtype)
    def __unicode__(self):
        return (u'%s') % (self.name)        
            

#医生Feild/Degree List
class TagList(models.Model):
    
    #1)Tag Type
    TYPE_CHOICES =(
        (u'F',_(u'Feild')),
        (u'D',_(u'Degree')),
        )    
    tagtype = models.CharField(max_length=1,blank=False,choices=TYPE_CHOICES)
    #2)DentistProfile as the ForeignKey
    dentistid = models.ForeignKey(DentistProfile)
    #3)Tag as the ForeignKey
    tagid = models.ForeignKey(Tag)
    
    def __unicode__(self):
        return (u'%s') % (self.tagid)
