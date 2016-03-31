# coding=utf-8
import re, os, cStringIO, Image
from utils import gen_guid
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db import transaction, connection
#
from relationship.models import Relationship
from public.views import _show_obj_name, _show_name
from imgupload.views import _uptoS3
from accounts.views import _put_wall_post
#
from stream.models import Post, Comment
from profile.models import Base
from django.contrib.auth.models import User
from iDentalk import settings
from django.utils import simplejson as json
from utils import JsonResponse, json_serialize, humantime


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def post_save(request):
    """
    This function post_save will save user's posts in db.
    @version 0.6
    """

    result = {}

    news = request.POST['post']
    news = news.strip()

    try:
        img_s = request.POST['img']
        img = img_s.replace('/s/', '/o/')
        img_m = img_s.replace('/s/', '/m/')
        print 'img is:', img
    except:
        img = img_s = img_m = ''
    try:
        url = request.POST['url']
    except:
        url = ''

    if len(news) > 600:
        result = {
                "status": False,
                "msg": "At most enter 600 characters."
        }

        return JsonResponse(result)

    else:
        news = re.sub('<', '&lt', news) # for tag <a>|</a>
        news = re.sub('>', '&gt', news)
        for m in re.finditer('https?://\S+|www\.\S+', news):
            news = re.sub(m.group(0), (r'<a href="%s">%s</a>') % (m.group(0), m.group(0)), news, count=1)
            print 'news after replace: ', news

        UserObj = User.objects.get(username = request.user)
        BaseObj = Base.objects.get(user=request.user)

        PostInsert = Post(post_content=news, img=img, img_s=img_s, img_m=img_m, url=url, comment_count=0, user_id=UserObj)
        PostInsert.save(force_insert=True)
        # _put_wall_post(request, news)

        post_id = PostInsert.id
        print "Insert Success!"

        PostObj = Post.objects.get(id=post_id)
        print(str(PostObj.post_date))
        result = {
                "status": True,
                "id": PostObj.id,
                "content": PostObj.post_content,
                "date": str(PostObj.post_date),
                "humandate": humantime(PostObj.post_date),
                "img_s": str(PostObj.img_s),
                "img_m": str(PostObj.img_m),
                "url": PostObj.url,
                "name":_show_name(request),
                "imagephoto": settings.MEDIA_URL + str(BaseObj.imagesmall),
        }

        return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def upload_post_img(request):
    image = request.FILES['img']
    if image.size > 2048000:
        result={
                    "status":False,
                    "toolarge":True,
                    "msg":"Your img is too big",
        }
        return HttpResponse( str(json.dumps(result)) )

    # global new_ext
    ext = os.path.splitext(image.name)[1].split('.')[1]
    # 由于PIL不能识别后缀名为jpg的文件，统一为jpeg格式
    if ext == 'jpg':
        ext = 'jpeg'
    elif ext == 'JPG':
        ext = 'jpeg'

    img = Image.open(image)
    ori_w, ori_h = img.size
    # box = (100, 100, 100, 100)
    # s_img = img.crop(box)
    if ori_w < 200 or ori_h < 150:
        s_size = ori_w, ori_h
        m_size = ori_w, ori_h
    else:
        s_rate = float(200) / float(ori_w)
        s_size = int(ori_w * s_rate), int(ori_h * s_rate)
        rate = float(490) / float(ori_w)
        m_size = int(ori_w * rate), int(ori_h * rate)

    s_img = img.resize(s_size, Image.ANTIALIAS)
    m_img = img.resize(m_size, Image.ANTIALIAS)

    s_cstr_out = cStringIO.StringIO()
    m_cstr_out = cStringIO.StringIO()
    cstr_out = cStringIO.StringIO()

    img.save(cstr_out, ext)
    s_img.save(s_cstr_out, ext)
    m_img.save(m_cstr_out, ext)

    guid = gen_guid()
    relative_url_path = 'post_img/o/' + guid
    s_relative_url_path = 'post_img/s/' + guid
    m_relative_url_path = 'post_img/m/' + guid

    img_wrap = [
        {
            'filename': s_relative_url_path,
            'filedir': s_cstr_out,
        },
        {
            'filename': relative_url_path,
            'filedir': cstr_out,
        },
         {
            'filename': m_relative_url_path,
            'filedir': m_cstr_out,
        },
    ]

    _uptoS3(img_wrap, ext)
    # _uptoS3(s_relative_url_path, s_cstr_out, ext)
    # _uptoS3(relative_url_path, cstr_out, ext)
    post_img_url = settings.MEDIA_URL + s_relative_url_path
    result = {
            "status":True,
            "post_img_url":post_img_url,
    }

    return HttpResponse( str(json.dumps(result)) )


@require_http_methods(["POST"])
@login_required
def _post_get(request, object_id, page):
    """
    This function _post_get will judge the user is himself or others,
    then decide to use which method to get user's posts from db 
    and sorting query result by time ascending, then make Postlist, return result.
    @version 0.4
    """

    Postlist = []

    # step for how many lines separate per page. then count nowa page's start line no. and end line no.
    step = 10
    end = step * int(page)
    start = step * (int(page)-1)
    is_end = False
    
    if object_id == "":
        total = Post.objects.filter(user_id=request.user).count()
        BaseObj = Base.objects.get(user=request.user)

        if (end - total) < step:
            is_end = False
            PostDict = Post.objects.filter(user_id=request.user).order_by('-id')[start:end]

            for PostObj in PostDict:
                Post_wrap = {
                        "id": PostObj.id,
                        "content": PostObj.post_content,
                        "date": str(PostObj.post_date),
                        "humandate": humantime(PostObj.post_date),
                        "img_s": str(PostObj.img_s),
                        "img_m": str(PostObj.img_m),
                        "url": PostObj.url,
                        "comments": PostObj.comment_count,
                        "is_end": is_end,
                        "name":_show_name(request),
                        "imagephoto": settings.MEDIA_URL + str(BaseObj.imagesmall),
                }

                Postlist.append(Post_wrap)

        else:
            is_end = True
            Post_wrap = {
                    "is_end": is_end
            }

            Postlist.append(Post_wrap)

    else:
        UserObj = User.objects.get(id=object_id)
        total = Post.objects.filter(user_id=UserObj).count()

        if (end - total) < step:
            is_end = False
            PostDict = Post.objects.filter(user_id=UserObj).order_by('-id')[start:end]

            for PostObj in PostDict:
                post_user = PostObj.user_id
                BaseObj = Base.objects.get(user=post_user)
                Post_wrap = {
                        "id": PostObj.id,
                        "content": PostObj.post_content,
                        "date": str(PostObj.post_date),
                        "humandate": humantime(PostObj.post_date),
                        "img": str(PostObj.img),
                        "img_s": str(PostObj.img_s),
                        "img_m": str(PostObj.img_m),
                        "url": PostObj.url,
                        "comments": PostObj.comment_count,
                        "is_end": is_end,
                        "name": _show_obj_name(post_user.id),
                        "imagephoto": settings.MEDIA_URL + str(BaseObj.imagesmall),
                }

                Postlist.append(Post_wrap)

        else:
            is_end = True
            Post_wrap = {
                    "is_end": is_end
            }

            Postlist.append(Post_wrap)

    return Postlist


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def post_get(request, object_id=""):
    """
    This function post_get will get user's posts from db sorting by time ascending
    through call function '_post_get' whether the request.user is himself or not.
    then response to browser to display
    @version 0.2
    """

    result = {}

    try:
        page = request.POST['page']
    except:
        page = 1

    result = _post_get(request, object_id, page)

    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST","GET"])
@login_required
def timeline_post_get(request):
    """
    This function timeline_post_get will get posts for this patient request.user
    from all followed by him in relationship, then display on Patient's homepage.
    @version 0.5
    """

    Postlist = []

    try:
        page = request.POST['page']
    except:
        page = 1

    step = 10
    end = step * int(page)
    start = step * (int(page)-1)
    is_end = False

    following = [entry.dentist for entry in Relationship.objects.filter(patient=request.user)] # patient's following lists
    print(following)

    total = Post.objects.filter(user_id__in=following).count()

    if (end - total) < step:
        is_end = False
        PostDict = Post.objects.filter(user_id__in=following).order_by('-id')[start:end]

        for PostObj in PostDict:
            post_user = PostObj.user_id
            BaseObj = Base.objects.get(user=post_user)

            Post_wrap = {
                    "id": PostObj.id,
                    "content": PostObj.post_content,
                    "date": str(PostObj.post_date),
                    "humandate": humantime(PostObj.post_date),
                    "img": str(PostObj.img),
                    "img_s": str(PostObj.img_s),
                    "img_m": str(PostObj.img_m),
                    "url": PostObj.url,
                    "comments": PostObj.comment_count,
                    "dentist_id": post_user.id,
                    # "name": post_user.last_name,
                    "name": _show_obj_name(post_user.id),
                    "imagephoto": settings.MEDIA_URL + str(BaseObj.imagesmall),
                    "is_end": is_end
            }

            Postlist.append(Post_wrap)

    else:
        is_end = True
        Post_wrap = {
            "is_end": is_end
        }
        
        Postlist.append(Post_wrap)

    return JsonResponse(Postlist)


@csrf_exempt
@require_http_methods(["POST","GET"])
@login_required
def notice_post_get(request, object_id):
    """
    This function notice_post_get will get posts for this dentist request.user
    from new comment Event, then display on a single post & comment homepage.
    @version 0.5
    """

    PostObj = Post.objects.get(id=object_id)
    CommentDict = Comment.objects.filter(post_id=PostObj)

    post_user = PostObj.user_id
    if post_user.id == request.user.id: # leave extend for patient go notice post page
        own = True
        identity = 'D'
    else:
        own = False
        identity = 'P'

    BaseObj = Base.objects.get(user=post_user)
    post_humandate=humantime(PostObj.post_date)

    Commentlist = []

    for CommentObj in CommentDict:

        comment_identity = Base.objects.get(user=CommentObj.user_id).identity

        Comment_wrap = {
                    "id": CommentObj.id,
                    "lastname": CommentObj.user_id.last_name, 
                    "content": CommentObj.comment_content, 
                    "date": CommentObj.comment_date,
                    "humandate": humantime(CommentObj.comment_date),
                    "comment_identity": comment_identity
        }

        Commentlist.append(Comment_wrap)

    result = {
            "own": own,
            "identity": identity,
            "imagephoto": settings.MEDIA_URL + str(BaseObj.imagesmall),
            "PostObj": PostObj,
            "post_humandate": post_humandate,
            "Commentlist": Commentlist
            }

    return render_to_response('notification/post.html', result,
                          context_instance=RequestContext(request))


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def post_delete(request):
    """
    This function post_delete will delete user's post and all comments
    for this post by dentist.
    @version 0.2
    """

    result = {}

    post_id = request.POST['pid']

    try:
        PostObj = Post.objects.get(id=post_id)
        Comment.objects.filter(post_id=PostObj).delete()
        PostObj.delete()

        result = {
                "status": True,
                "msg": 'Deleted'
        }
    except:
        result = {
                "status": False,
                "msg": "failure"
        }

    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def comment_save(request):
    """
    This function comment_save will save user's comments for this post.
    @version 0.5
    """

    result = {}

    user = request.user
    print(request.user.username)
    UserObj = User.objects.get(username=user)

    print request.POST
    pid = request.POST['pid']
    comment = request.POST['comment']
    comment = comment.strip()

    if len(comment) > 600:
        result = {
                "status": False,
                "msg": "At most enter 600 characters."
        }

        return JsonResponse(result)

    else:
        ip = request.META['REMOTE_ADDR']

        PostObj = Post.objects.get(id = pid)
        comment_count_bef = PostObj.comment_count
        comment_count = comment_count_bef + 1

        Post.objects.filter(id = pid).update(comment_count=comment_count)
        print "Post Update Success!"
        PostObj_new = Post.objects.get(id = pid)

        CommentInsert = Comment(comment_content=comment, comment_author_ip=ip,
                                user_id=user, post_id=PostObj_new)
        CommentInsert.save(force_insert=True)

        CommentObj = Comment.objects.get(id=CommentInsert.id)
        print(str(CommentObj.comment_date))
        print(CommentObj.comment_date)
        print "Comment Insert Success!"
        comment_identity = Base.objects.get(user=CommentObj.user_id).identity

        result = {
                "status": True,
                "id": CommentObj.id,
                "content": CommentObj.comment_content,
                "date": str(CommentObj.comment_date),
                "humandate": humantime(CommentObj.comment_date),
                "username": user.last_name,
                "comment_count": PostObj_new.comment_count,
                "comment_identity": comment_identity
        }

        return JsonResponse(result)


@require_http_methods(["POST"])
@login_required
def _comment_get(request, object_id, post_id):
    """
    This function _comment_get will get user's comments for post_id post from db
    sorting by time ascending, and make Commentlist and return.
    @version 0.5
    """

    user = request.user
    Commentlist = []

    if object_id == "":
        CommentDict = Comment.objects.filter(post_id=post_id)

        for CommentObj in CommentDict:
            UserObj = CommentObj.user_id
            comment_identity = Base.objects.get(user=CommentObj.user_id).identity

            Comment_wrap = {
                    "id": CommentObj.id,
                    "content": CommentObj.comment_content,
                    "date": str(CommentObj.comment_date),
                    "humandate": humantime(CommentObj.comment_date),
                    "username": UserObj.last_name,
                    "own": True,
                    "comment_identity": comment_identity
            }

            Commentlist.append(Comment_wrap)

    else:
        UserObj = User.objects.get(id=object_id)
        CommentDict = Comment.objects.filter(user_id=UserObj)
        

        for CommentObj in CommentDict:
            UserObj = CommentObj.user_id
            comment_identity = Base.objects.get(user=CommentObj.user_id).identity

            Comment_wrap = {
                    "id": CommentObj.id,
                    "content": CommentObj.comment_content,
                    "date": str(CommentObj.comment_date),
                    "humandate": humantime(CommentObj.comment_date),
                    "username": UserObj.last_name,
                    "own": False,
                    "comment_identity": comment_identity
            }

            Commentlist.append(Comment_wrap)

    return Commentlist


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def comment_get(request, object_id=""):
    """
    This function comment_get will get user's posts from db sorting by time ascending,
    whether the request.user is himself or not, and display On Dentist's Page
    @version 0.2
    """

    result = {}

    post_id = request.POST['post_id']

    result = _comment_get(request, object_id, post_id)

    return JsonResponse(result)


# from django.core.cache.backends.memcached import CacheClass
# memcli = CacheClass( '127.0.0.1:11211', ?which parameter)
# import memcache
# memcli = memcache.Client(['127.0.0.1:11211'], debug=1)
@csrf_exempt
@require_http_methods(["POST","GET"])
@login_required
def timeline_comment_get(request):
    """
    This function timeline_comment_get will get comments for this post_id post
    from db, and display On Patient's Page
    @version 0.3
    """

    user = request.user
    Commentlist = []
    post_id = request.POST['post_id']

    CommentDict = Comment.objects.filter(post_id=post_id)

    for CommentObj in CommentDict:
        UserObj = CommentObj.user_id
        comment_identity = Base.objects.get(user=CommentObj.user_id).identity

        Comment_wrap = {
                "id": CommentObj.id,
                "content": CommentObj.comment_content,
                "date": str(CommentObj.comment_date),
                "humandate": humantime(CommentObj.comment_date),
                "username": UserObj.last_name,
                # "own": True,
                "comment_identity": comment_identity
        }

        Commentlist.append(Comment_wrap)

    return JsonResponse(Commentlist)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def comment_delete(request):
    """
    This function comment_delete will delete user's comment for this post by dentist.
    @version 0.3
    """

    result = {}
    cid = request.POST['cid']

    try:
        CommentObj = Comment.objects.get(id=cid)
        PostObj = CommentObj.post_id
        CommentObj.delete()

        comment_count_bef = PostObj.comment_count
        comment_count = comment_count_bef - 1

        PostObj.comment_count = comment_count
        PostObj.save(force_update=True)

        result = {
                "status": True,
                "msg": "Success",
                "pid": PostObj.id,
                "comment_count": PostObj.comment_count
                }
    except:
        result = {
                "status": False,
                "msg": "Failure"
                }

    return JsonResponse(result)
