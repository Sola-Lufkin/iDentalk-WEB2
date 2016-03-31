# -*- coding: utf8 -*-
import math, decimal
import sys

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User 
from iDentalk import settings

from public.views import _show_obj_name
from den_manage.views import _relation_counts
from annoying.decorators import render_to, ajax_request
from profile.models import WorkPlace, PatientProfile, DentistProfile, Base
from decorators import require_identity_type
from utils import JsonResponse
from django.utils import simplejson as json


@csrf_exempt
@require_identity_type("Patient")  # the empty search page
@render_to('search/search_geoloc_range_fixed_loc.html')
def search_geoloc_range_fixed_loc(request):
    """ fixed location empty page """

    patient_profile = PatientProfile.objects.get(user=request.user)
    fixed_location = patient_profile.location

    latitude = str(patient_profile.latitude)
    longitude = str(patient_profile.longitude)
    latlng = "("+latitude+", "+longitude+")"
    print latlng
    
    template_var = {
                "mylocation": fixed_location,
                "latlng": latlng
    }

    return template_var


@csrf_exempt
# @require_identity_type("Patient")    # the empty search page
@render_to('search/search_geoloc_range_free_loc.html')
def search_geoloc_range_free_loc(request):
    """ free location empty page """

    template_var = {
    }

    return template_var


@csrf_exempt
@require_http_methods(["POST", "GET"])
def search_geoloc_range(request):
    """ return the dentist list which belong to the patient's geolocation range """

    distance = float(request.POST['distance'])

    latlng = (request.POST['latlng']).replace("(",'').replace(")",'').split(', ')
    latitude = float(latlng[0])
    longitude = float(latlng[1])
    print distance
    print latitude
    print longitude

    # count range of nowa latlng
    radius_lat = (distance/(69.172))  #count latitude range
    min_lat = latitude - radius_lat
    max_lat = latitude + radius_lat
    print min_lat
    print max_lat

    radius_lng = (math.fabs(distance/(math.cos(longitude) * 69.172))) #count longitude range
    min_lng = longitude - radius_lng
    max_lng = longitude + radius_lng
    print min_lng
    print max_lng

    # if sys.version_info < (2, 7):
    #     min_lat = decimal.Decimal(str(min_lat))
    #     max_lat = decimal.Decimal(str(max_lat))
    #     min_lng = decimal.Decimal(str(min_lng))
    #     max_lng = decimal.Decimal(str(max_lng))

    # query db to match the range of dentist work place in db
    total = WorkPlace.objects.filter(latitude__gte=min_lat, latitude__lte=max_lat,
                                    longitude__gte=min_lng, longitude__lte=max_lng).count()

    result = []

    # step for how many lines separate per page. then count nowa page's start line no. and end line no.
    if 'page' in request.POST:
        page = request.POST['page']
    else:
        page = 1

    step = 10
    end = step * int(page)
    start = step * (int(page)-1)
    is_end = False

    if (end - total) < step:
        is_end = False
        WorkPlaceDict = WorkPlace.objects.filter(latitude__gte=min_lat, latitude__lte=max_lat,
                        longitude__gte=min_lng, longitude__lte=max_lng).order_by('id')[start:end]

        for i in WorkPlaceDict:

            dentist_profile = i.dentistid
            did = dentist_profile.user.user.id

            latitude = str(i.latitude)
            longitude = str(i.longitude)
            latlng = "("+latitude+", "+longitude+")"

            counts = _relation_counts(request,did,request.user.id)

            i_wrap = {
                    "clinic": i.clinic_name,
                    "work_location": i.location,
                    "latlng": latlng,
                    "business_hour": str(i.business_hour),
                    "dentistid": did,
                    "dentistname": _show_obj_name(did),
                    "summary": dentist_profile.user.summary,
                    "avatar": settings.MEDIA_URL + str(dentist_profile.user.imagesmall),
                    "patient_count": counts["patient_count"],
                    "follower_count": counts["follower_count"],
                    "status": counts["status"],
                    "is_end": is_end
            }

            result.append(i_wrap)

    else:
        is_end = True
        i_wrap = {
            "is_end": is_end
        }

        result.append(i_wrap)

    template_var = {
                "searchresult": result
    }

    return JsonResponse(template_var)


####  name based search!!!!!
@csrf_exempt
def search_by_name(request):
    """ serve for patient top navigation name based search form && search name page ajax request """
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        try: 
            identity = Base.objects.get(user=request.user).identity
        except:
            identity = 'AnonymousUser'
        template_var = {
                     "identity":identity,
                     "keyword":keyword,
        }
        print identity
        return render_to_response('search/search_by_name.html', template_var,
                          context_instance=RequestContext(request))

    else:
        if 'data' in request.GET:
            data = json.loads(request.GET['data'])
            keyword = data['keyword']

            searchresult = _searchresult_name(request, keyword=keyword)
            template_var = {
                        "searchresult":searchresult,
            }
        else:
            return render_to_response('search/search_by_namae.html',template_var,
                          context_instance=RequestContext(request))

        return JsonResponse(template_var)


def _searchresult_name(request, keyword=""):
    """ """

    #按照空格切分kkeyword,用于判断用户录入的keyword类型，切分后个数小于2，说明用户录入只一个单一keyword，否则为多个
    keyword=keyword.strip().split()

    if 'page' in json.loads(request.GET['data']):
        page = json.loads(request.GET['data'])["page"]
        print page
    else:
        page = 1

    step = 10
    end = step * int(page)
    start = step * (int(page)-1)
    is_end = False

    searchresult = []

    ##该方法下的姓名搜索，搜索结果为 姓 或者 名 匹配便出现在搜索集合中
    if len(keyword)<2:
        # One Keyword
        total = (User.objects.filter(first_name=keyword[0], is_active=True) | User.objects.filter(last_name=keyword[0], is_active=True)).count()
        if (end - total) < step:
            results = (User.objects.filter(first_name=keyword[0], is_active=True) | User.objects.filter(last_name=keyword[0], is_active=True))[start:end]
            for i in results:       
                base = Base.objects.get(user=i)
                # try:
                ##Bug 如果医生没有诊所，也应该显示出来信息
                if base.identity == "D":
                    dentist = DentistProfile.objects.get(user=i)
                    counts = _relation_counts(request,i.id,request.user.id)
                    WorkPlaceQuery = WorkPlace.objects.filter(dentistid = dentist)
                    # print counts["status"]
                    dentistinfo = {

                                    "dentistid":i.id,
                                    "dentistname":_show_obj_name(i.id),
                                    "summary":base.summary,
                                    "avatar":settings.MEDIA_URL + str(base.imagesmall),
                                    "patient_count":counts["patient_count"],
                                    "follower_count":counts["follower_count"],
                                    "status":counts["status"],
                                    "is_end": is_end,
                    }
                    ##如果workplace的个数大于0，便添加place信息
                    if dentist.workplace_count > 0:
                        
                        placeinfo= {
                                    "clinic_name":WorkPlaceQuery[0].clinic_name,
                                    "work_location":WorkPlaceQuery[0].location,
                                    "business_hour": str(WorkPlaceQuery[0].business_hour),
                                    "have_clinic":True,
                        }

                        dentistinfo.update(placeinfo)
                    else:
                        placeinfo= {
                                    # "clinic_name":"None",
                                    # "work_location":"None",
                                    # "start":"None",
                                    # "end":"None",
                                    "have_clinic":False,
                        }

                        dentistinfo.update(placeinfo)

                    searchresult.append(dentistinfo)


        else:
            is_end = True
            i_wrap = {
                "is_end": is_end
            }

            searchresult.append(i_wrap)
    else:
        # Two keyword
        total = (User.objects.filter(first_name=keyword[0], last_name=keyword[1], is_active=True) | User.objects.filter(first_name=keyword[1], last_name=keyword[0], is_active=True)).count()
        if (end - total) < step:
            is_end = False
            results = (User.objects.filter(first_name=keyword[0], last_name=keyword[1], is_active=True) | User.objects.filter(first_name=keyword[1], last_name=keyword[0], is_active=True))[start:end]
            for i in results:   
                base = Base.objects.get(user=i)
                # try:
                ##Bug 如果医生没有诊所，也应该显示出来信息          
                if base.identity == "D":
                    dentist = DentistProfile.objects.get(user=i)
                    counts = _relation_counts(request,i.id,request.user.id)
                    WorkPlaceQuery = WorkPlace.objects.filter(dentistid = dentist)
                    # print counts["status"]
                    dentistinfo = {
                                    "dentistid":i.id,
                                    "dentistname":_show_obj_name(i.id),
                                    "summary":base.summary,
                                    "avatar":settings.MEDIA_URL + str(base.imagesmall),
                                    "patient_count":counts["patient_count"],
                                    "follower_count":counts["follower_count"],
                                    "status":counts["status"],
                                    "is_end": is_end,
                    }
                    ##如果workplace的个数大于0，便添加place信息
                    if dentist.workplace_count > 0:
                        
                        placeinfo= {
                                    "clinic_name":WorkPlaceQuery[0].clinic_name,
                                    "work_location":WorkPlaceQuery[0].location,
                                    "business_hour": str(WorkPlaceQuery[0].business_hour),
                        }

                        dentistinfo.update(placeinfo)

                    searchresult.append(dentistinfo)
                    
                        
                    
        else:
            is_end = True
            i_wrap = {
                "is_end": is_end
            }

            searchresult.append(i_wrap)

    return searchresult
