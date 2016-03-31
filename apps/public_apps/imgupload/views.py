# -*- coding: utf8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _   ####
#from PIL import Image
import Image
from Image import EXTENT
import os, string, cStringIO
from utils import gen_guid
from iDentalk import settings

from profile.forms import ImgForm
from profile.models import *
from settings import BASE_DIR

def _uptoS3(obj, ext):
    from boto.s3.connection import S3Connection   
    try:
        # global conn 
        conn = S3Connection(settings.S3_ACCESS_KEY,settings.S3_SECRET_KEY)
        print 'defined conn'
        bucket = settings.S3_BUCKET
        from boto.s3.key import Key
        from hashlib import md5
        b = conn.get_bucket(bucket)
        print 'connect to S3 via conn'
        k = Key(b)
        print 'connect to Key'

        print 'loop to save item in obj'
        for i in obj:
            print 'new loop'
            k.key = i['filename']
            print 'defined k.key'

            print 'start upload to S3'
            k.set_contents_from_string(i['filedir'].getvalue(), policy='public-read')
            print 'finish uploaded'

            print 'set metadata value'
            if ext=='jpeg' :
                type_value='image/jpeg'     
            elif ext=='png' or ext=='PNG':
                type_value='image/png'
            elif ext=='gif' or ext=='GIF':
                type_value='image/gif'
            elif ext=='bmp' or ext=='BMP':
                type_value='image/bmp'
            k = k.copy(k.bucket.name, k.name, {'Content-Type':type_value}, preserve_acl=True)
            print 'finish setting metadata value'
            ## the content-type of img on S3 can't be added automatically, so here is the way to add the type for img
        k.close()
        print 'close key'

    except IOError, e:
        print "No works"
    else:
        print "works"

def _getfromS3(s3_path,local_file):  
    from boto.s3.connection import S3Connection   
    try:
        conn = S3Connection(settings.S3_ACCESS_KEY,settings.S3_SECRET_KEY)
        bucket = settings.S3_BUCKET
        from boto.s3.key import Key
        # from hashlib import md5
        print 'start to connect S3'       
        b = conn.get_bucket(bucket)
        print 'connected to S3 via conn'
        key = b.lookup(s3_path)  
        print 'connected to Key'
        key.get_contents_to_filename(local_file)      
    except IOError, e:
       print "No works"
    else:
       print "works"

def _delfromS3(filename):
    from boto.s3.connection import S3Connection   
    try:
        conn = S3Connection(settings.S3_ACCESS_KEY,settings.S3_SECRET_KEY)
        bucket = settings.S3_BUCKET
        from boto.s3.key import Key
        b = conn.get_bucket(bucket)
        k = Key(b)
        k.key = filename
        b.delete_key(k)  
    except IOError, e:
       print "No works"
    else:
       print "works"  


def _imgupload(request,UserProfile):
    '''头像上传'''
    
    if request.method=="POST":
        UserProfileObj=UserProfile.objects.get(user=request.user)
        #if it's the  first time user upload his photo,we make a new guid, otherwise we copy the old guid.
        #replace the old img on S3 by this way
        if UserProfileObj.imagephoto.name == 'site_static/img/8.png':
           guid=gen_guid()
        else:
           guid=UserProfileObj.imagephoto.name.replace('userphoto/head_nature_','')

        if 'imagephoto' in request.FILES:   #imagephoto为对应的HTML输入框的name属性值
           image = request.FILES["imagephoto"]
           # way to make sure the uploaded file less than 2M 
           if image.size > 2048000:
              print "size is too large"
              img_data={
                        "toolarge":True,
               }
              return img_data

           print image.size
           img= Image.open(image)
           w,h=img.size
           # count out the new size for font-end displaying
           # if w > h:
           #      rate = float(250) / float(w)
           # else:
           #      rate = float(250) / float(h)
           # new_size = (int(w*rate),int(h*rate))
           # keep the width size, change th height size
           rate = float(250) / float(w)
           new_size = (int(w*rate),int(h*rate))

           #we upload original-size img to S3 without shrinking 
           # img = img.resize(new_size, Image.BILINEAR)

           #得到上传的文件的后缀名
           ext = os.path.splitext(image.name)[1].split('.')[1]
           #由于PIL不能识别后缀名为jpg的文件，一旦遇到形如jpg的后缀名，自动替换成jpeg
           if ext=='jpg':
                ext='jpeg'
           elif ext=='JPG':
                ext='jpeg' 
           #NOTE, we're saving the image into a cStringIO object to avoid writing to disk
           out_im1 = cStringIO.StringIO()
           #You MUST specify the file type because there is no file name to discern it from
           img.save(out_im1,ext)

           #here we're saving the user's Imagephoto to S3, the variable 'filename' is the url on S3
           filename='userphoto/'+'head_nature_'+guid

           _uptoS3([
                {
                'filename': filename,
                'filedir': out_im1,
                }
            ], ext)

           #saving every detail data of Imagephoto to database
           UserProfileObj.imagephoto=filename
           #pic_ext will be used in _imgcut
           UserProfileObj.pic_ext = ext
           UserProfileObj.save()
           print 'here is the size'
           print w
           print h
           print new_size[0]
           print new_size[1]
           img_data={
                    "url":filename,
                    "width":new_size[0],
                    "height":new_size[1],
                    "toolarge": False,
           }
    return img_data   


def _imgcut(request,UserProfile,data):
    '''头像剪切'''
     
    if request.method=="POST":

        UserProfileObj=UserProfile.objects.get(user=request.user)
        #因為只能在本地而不能在遠程S3上處理圖片，因此需要將圖片從S3上下載至本地處理
        #！！！！往往會因為路徑問題，在下載這個過程中出現錯誤導致整個頭像剪切過程失敗
        #
        print 'get imagephoto from S3' 
        image = UserProfileObj.imagephoto
        #ext is a field that save the ext of the img user upload to S3, if we get the simple way to get the metadata from S3
        #this field will be droped.
        ext = UserProfileObj.pic_ext
        guid = image.name 
        guid = guid.replace('userphoto/head_nature_','')
        #local_file is the path, the img from S3 will be download to
        local_file =settings.MEDIA_ROOT+image.name
        #here the value of the image equal to the file-path on S3
        s3_path=image.name
        # download the image from S3 for img-cutting
        _getfromS3(s3_path,local_file)

        print 'ready for opening imagephoto'
        #open the counterpart of the image which would be cutted
        #in this way, we can open the image on disk  
        img= Image.open(image) ##打开图片
        w,h=img.size
        rate = float(w) / float(250)
        new_size = (int(w*rate),int(h*rate))
        
        print 'opened'

        #頭像剪切在下面的剪切過程中出現了特別嚴重的遲鈍,延遲的原因完全是上傳至S3服務器時太慢所導致
        print w
        print h
        print data["x1"]
        print data["x2"]
        print data["y1"]
        print data["y2"]
        x1 = float(data["x1"])*rate
        x2 = float(data["x2"])*rate
        y1 = float(data["y1"])*rate
        y2 = float(data["y2"])*rate
        print x1
        print x2
        print y1
        print y2
        img=img.transform((250,250),
                          EXTENT,
                          (string.atof(x1),string.atof(y1),string.atof(x2),string.atof(y2)),Image.BICUBIC
                         ) #需要将字符串转换成整型后再赋值
        
        print 'img-cut is over,lets shrink & save it'
        #the way to upload to S3
        #NOTE, we're saving the image into a cStringIO object to avoid writing to disk
        out_im2 = cStringIO.StringIO()
        #You MUST specify the file type because there is no file name to discern it from
        img.save(out_im2,ext,quality=90)
        filename2='userphoto/'+'head_250_250_'+guid
        # _uptoS3(filename,out_im2,ext)     
        UserProfileObj.imagebig=filename2 
        UserProfileObj.save() 

        '''头像缩小'''
    
        print 'lets get thumbnail(100,100)'
        img.thumbnail((100,100),Image.ANTIALIAS) ###对图片进行处理大小
        print 'thumbnail got'
        out_im3 = cStringIO.StringIO()
        img.save(out_im3,ext,quality=90)
        filename3='userphoto/'+'head_100_100_'+guid

        # _uptoS3(filename,out_im3,ext)        
        
        print 'now saving them to S3'
        _uptoS3([
            {
                'filename': filename2,
                'filedir': out_im2,
            },
            {
                'filename': filename3,
                'filedir': out_im3,
            }
        ], ext)

        UserProfileObj.imagesmall=filename3                
        UserProfileObj.save()
        #完成圖片處理後，刪除掉下載至本地的圖片
        os.remove(BASE_DIR+'/uploaded'+'/userphoto/head_nature_'+guid)
