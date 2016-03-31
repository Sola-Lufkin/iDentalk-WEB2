# coding=utf-8
import os, Image, cStringIO
#
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_control
from django.utils import simplejson as json
from django.db import transaction
from django.contrib.auth.models import User
#
from imgupload.views import _uptoS3, _delfromS3
from annoying.decorators import render_to, ajax_request
from gallery.models import Case, CaseImg
from profile.models import DentistProfile,Base
from gallery.forms import CaseImgForm, CaseDescForm
from iDentalk import settings
from utils import JsonResponse, json_serialize, gen_guid
from annoying.decorators import render_to, ajax_request
from decorators import require_identity_type


@cache_control(must_revalidate=True, max_age=3600)
@csrf_exempt
@login_required
def case_list(request, uid = ""):
    """
    This function case_list will return all case list as json data
    @version 0.3
    """

    if uid == "":
        CaseDict = Case.objects.filter(dentistid=request.user)[:9]
        uid = request.user.id
        is_private = True
    else:
        UserObj = User.objects.get(id=uid)
        CaseDict = Case.objects.filter(dentistid=UserObj)
        uid = uid

    Caselist = []

    for CaseObj in CaseDict:

        Case_wrap = {
                "id": CaseObj.id,
                "case_name": CaseObj.case_name,
                "uid": uid,
        }

        ## if user do not upload any case img, we show the warns
        try:
            CaseImgObj = CaseImg.objects.filter(caseid=CaseObj)[0]
            Case_wrap["bef_img"] = settings.MEDIA_URL + str(CaseImgObj.bef_img)
            Case_wrap["aft_img"] = settings.MEDIA_URL + str(CaseImgObj.aft_img)
            Case_wrap["status"] = 1
        except:
            pass
            Case_wrap["status"] = 0

        Caselist.append(Case_wrap)

    return JsonResponse(Caselist)
    

@cache_control(must_revalidate=True, max_age=3600)
@render_to("gallery/case_list.html")
@require_http_methods(["GET"])
def case_list_big(request, uid = ""):
    """
    This function case_list_big will render all case list with description
    @version 0.3
    """

    template_var = {}

    try:
        UserObj = User.objects.get(id=uid) 
        CaseDict = Case.objects.filter(dentistid=UserObj)
        if UserObj == request.user:
            is_private = True
        else:
            is_private = False

        Caselist = []

        for CaseObj in CaseDict:                   
            try:
                CaseImgObj = CaseImg.objects.filter(caseid=CaseObj).order_by('id')[0]
                bef_img = settings.MEDIA_URL + str(CaseImgObj.bef_img)
                aft_img = settings.MEDIA_URL + str(CaseImgObj.aft_img)
            except:
                ##没有图片便显示默认图片，并提示用户上传
                bef_img = "/site_static/img/head_50_50.png"
                aft_img = "/site_static/img/head_50_50.png"

            Case_wrap = {
                    "id": CaseObj.id,
                    "case_name": CaseObj.case_name,
                    "description": CaseObj.description,
                    "bef_img": bef_img,
                    "aft_img": aft_img,
            }

            Caselist.append(Case_wrap)

        template_var = {
                        'Caselist':Caselist,
                        'is_private':is_private,
                        'uid':uid,
        }
    except:
        ## If user do not upload any cases now, show blank page    
        template_var = { 
                        'msg':'No Cases now',
                        'is_private':is_private,
                        'uid':uid,
        }

    return template_var


@render_to("gallery/case_detail.html")
@require_http_methods(["GET"])
def case_detail(request, uid, case_id):
    """
    This function case_detail will render detail info for one case.
    @version 0.3
    """

    CaseObj = Case.objects.get(id=case_id) 
    CaseImgDict = CaseImg.objects.filter(caseid=CaseObj)

    if request.user ==CaseObj.dentistid.user.user:
        is_private = True
    else:
        is_private = False

    result = {
                "is_private": is_private,
                "CaseObj": CaseObj,
                "CaseImgDict": CaseImgDict,
                "owner":CaseObj.dentistid.user.user,
    }

    return result


def _case_img_upload(request, bef_img, aft_img):
    """
    This function _case_img_upload will save Case Image in the file system and
    return web system url after submit
    @version 0.6
    """
    
    ext = os.path.splitext(bef_img.name)[1].split('.')[1]
    # 由于PIL不能识别后缀名为jpg的文件，统一为jpeg格式
    if ext == 'jpg':
        ext = 'jpeg'
    elif ext == 'JPG':
        ext = 'jpeg'

    img = Image.open(bef_img)
    cstr_out_bef = cStringIO.StringIO()
    img.save(cstr_out_bef, ext)

    guid_bef = gen_guid()
    relative_url_path_bef = 'gallery/' + 'case_img_' + guid_bef

    ext = os.path.splitext(aft_img.name)[1].split('.')[1]
    # 由于PIL不能识别后缀名为jpg的文件，统一为jpeg格式
    if ext == 'jpg':
        ext = 'jpeg'
    elif ext == 'JPG':
        ext = 'jpeg'

    img = Image.open(aft_img)
    cstr_out_aft = cStringIO.StringIO()
    img.save(cstr_out_aft, ext)

    guid_aft = gen_guid()
    relative_url_path_aft = 'gallery/' + 'case_img_' + guid_aft
    _uptoS3([
        {
            "filename": relative_url_path_bef,
            "filedir": cstr_out_bef,
        },
        {
            "filename": relative_url_path_aft,
            "filedir": cstr_out_aft,
        }
    ], ext)

    relative_url_path = [relative_url_path_bef, relative_url_path_aft]

    return relative_url_path


@csrf_exempt
@require_http_methods(["POST"])
@login_required
@require_identity_type('Dentist')
def case_base_add(request):
    """
    This function case_base_add will save the user input in the Case form after submit
    @version 0.3
    """

    result = {}
    
    data = json.loads(request.POST['data'])
    case_name = data['case_name']
    description = data['description']
    case_name = case_name.strip()
    description = description.strip()

    if len(case_name) > 64:
        result = {
                "status": False,
                "msg": "At most enter 64 characters."
        }

        return JsonResponse(result)

    elif len(description) > 256:
        result = {
                "status": False,
                "msg": "At most enter 256 characters."
        }

        return JsonResponse(result)

    else:
        DentistObj = DentistProfile.objects.get(user=request.user)
        CaseInsert = Case(case_name=case_name, description=description, img_count=0, dentistid=DentistObj)

        try:
            CaseInsert.save(force_insert=True)
            case_id = CaseInsert.id
            
            result = {
                        "status": True,
                        "msg": "saved",
                        "case_id": case_id
                    }
        except:
            result = {"msg": "failure"}

        return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
@require_identity_type('Dentist')
def case_img_add(request):
    """
    This function case_img_add will save the user input in the Case Image form after submit
    @version 0.2
    """

    result = {}

    bef_img = request.FILES['bef_img']
    aft_img = request.FILES['aft_img']
    if bef_img.size > 2048000 or aft_img.size > 2048000:
        print "size is too large"
        result = {  
                    "status": False,
                    "msg": "Your img is too big", 
                    "toolarge": True,
                }
        return HttpResponse( str(json.dumps(result)) )

    case_id = request.POST['case_id']

    bef_img_url,  aft_img_url = _case_img_upload(request, bef_img, aft_img) 
    CaseObj = Case.objects.get(id = case_id)
    CaseImgInsert = CaseImg(bef_img=bef_img_url, aft_img=aft_img_url, caseid=CaseObj)

    try:
        CaseImgInsert.save(force_insert=True)
        CaseImg_id = CaseImgInsert.id
        result = {  
                    "status": True,
                    "msg": "Success", 
                    "bef_img": settings.MEDIA_URL + bef_img_url, 
                    "aft_img": settings.MEDIA_URL + aft_img_url,
                    "img_id": CaseImg_id
                }
    except:
        result = {"status": False}
        
    return HttpResponse( str(json.dumps(result)) )


@csrf_exempt
@require_http_methods(["POST"])
@login_required
@require_identity_type('Dentist')
def case_info_update(request):
    """
    This function case_name_update will save these case name updated by user in case detail page
    @version 0.3
    """

    result = {}
    
    data = json.loads(request.POST['data'])
    case_name = data['case_name']
    description = data['description']
    case_id = data['case_id']
    case_name = case_name.strip()
    description = description.strip()

    if len(case_name) > 64:
        result = {
                "status": False,
                "msg": "At most enter 64 characters."
        }

        return JsonResponse(result)

    elif len(description) > 256:
        result = {
                "status": False,
                "msg": "At most enter 256 characters."
        }

        return JsonResponse(result)

    else:
        try:
            Case.objects.filter(id=case_id).update(case_name=case_name, description=description)
            result = {
                        "status": True,
                        "msg": "saved", 
                    }
        except:
            result = {"msg": "failure"}

        return JsonResponse(result)


def _case_img_remove(img_url):
    """
    This function _case_img_remove will delete Case Image from given path in the file system
    @version 0.1
    """

    path = settings.MEDIA_ROOT + img_url
    print(path)
    os.remove(path)


# @csrf_exempt
# @require_http_methods(["POST"])
# @login_required
# def case_img_update(request):
#     """
#     This function case_img_update will save these images updated by user in case detail page,
#     but now we use case_img_add to update images
#     @version 0.3

#     leave for next use!!!
#     """

#     result = {}

#     bef_img = request.FILES['bef_img']
#     aft_img = request.FILES['aft_img']
#     case_id = request.POST['case_id']

#     bef_img_url = _case_img_upload(request, bef_img)
#     aft_img_url = _case_img_upload(request, aft_img)

#     CaseObj = Case.objects.get(id = case_id)
#     CaseImgDict = CaseImg.objects.filter(caseid=CaseObj)

#     for CaseImgObj in CaseImgDict:
#         bef_img_url_rm = str(CaseImgObj.bef_img)
#         aft_img_url_rm = str(CaseImgObj.aft_img)
#         _case_img_remove(bef_img_url_rm)
#         _case_img_remove(aft_img_url_rm)

#     CaseImgUpdate = CaseImg(bef_img=bef_img_url, aft_img=aft_img_url, caseid=CaseObj)

#     try:
#         CaseImgUpdate.save(force_update=True)
#         CaseImg_id = CaseImgUpdate.id
#         result = {  
#                     "status": True,
#                     "msg": "success", 
#                     "bef_img": settings.MEDIA_URL + bef_img_url, 
#                     "aft_img": settings.MEDIA_URL + aft_img_url,
#                     "img_id": CaseImg_id
#                 }
#     except:
#         result = {"status": False}
        
#     return HttpResponse( str(json.dumps(result)) )


@csrf_exempt
@login_required
@require_identity_type('Dentist')
def case_delete(request):
    """
    This function case_delete will delete the case in case detail page
    @version 0.3
    """

    result = {}

    case_id = request.POST['case_id']
    CaseObj = Case.objects.get(id=case_id)

    try:
        CaseImgDict = CaseImg.objects.filter(caseid=CaseObj)

        for CaseImgObj in CaseImgDict:
            bef_img_url = str(CaseImgObj.bef_img)
            aft_img_url = str(CaseImgObj.aft_img)
            _delfromS3(bef_img_url)
            _delfromS3(aft_img_url)

        CaseImgDict.delete()
        Case.objects.get(id=case_id).delete()

        result = {
                    "msg":"Success",
                    "status": True,
        }
    except:
        result = {
                    "msg":"Failure",
                    "status": False,
        }

    return JsonResponse(result)


@csrf_exempt
@login_required
def case_img_delete(request):
    """
    This function case_img_delete will delete this pair of images in case detail page
    where user click delete button
    @version 0.3
    """

    result = {}

    CaseImg_id = request.POST["img_id"]

    try:
        CaseImgObj = CaseImg.objects.get(id=CaseImg_id)

        bef_img_url = str(CaseImgObj.bef_img)
        aft_img_url = str(CaseImgObj.aft_img)
        _delfromS3(bef_img_url)
        _delfromS3(aft_img_url)

        CaseImgObj.delete()

        result = {
                    "msg":"Success",
                    "status": True,
        }
    except:
        result = {
                    "msg":"Failure",
                    "status": False,
        }

    return JsonResponse(result)
