# -*- coding: utf8 -*-
import re, urllib, urllib2, httplib

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json
from utils import JsonResponse
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout #调用时重命名login和logout，以防止命名冲突
from django.utils.translation import ugettext_lazy as _  #支持多语言翻译

from accounts.forms import PasswordChangeForm
from registration.views import activate as regis_activate
from registration.views import register
from forms import LoginForm, LoginAgainForm
from profile.models import Base, DentistProfile, PatientProfile
from annoying.decorators import render_to, ajax_request
import settings
#from captcha.views import create_validate_code


def _show_name(request):
    '''返回当前登录用户自己的姓名信息'''

    UserObj = User.objects.get(username=request.user)
    BaseObj = Base.objects.get(user=request.user)
    myname = ""
    
    # if BaseObj.show_mid_name:
    #     myname = UserObj.first_name +" "+ BaseObj.middle_name +" "+ UserObj.last_name
    #     return myname
    # else:
    myname = UserObj.first_name +" "+ UserObj.last_name
    return myname

@require_http_methods(["GET", "POST"])
def login(request,template_name):
    '''带页面的登陆视图'''

    template_var={}
    form = LoginForm()  
    # if request.method == 'POST':
    form=LoginForm(request.POST.copy())
    if form.is_valid():
        if _login(request,form.cleaned_data["username"],form.cleaned_data["password"]) == True :
            return HttpResponseRedirect(reverse("is_first_login"))
        else:
            return HttpResponseRedirect(reverse("login_again"))
            
    template_var["form"]=form        
    return render_to_response(template_name,template_var,context_instance=RequestContext(request)) 


@require_http_methods(["GET", "POST"])
def loginfunction(request):
    '''无页面的登陆函数''' 

    form = LoginForm()
    if request.method == 'POST':
        form=LoginForm(request.POST.copy())
        if form.is_valid():
            if _login(request,form.cleaned_data["username"],form.cleaned_data["password"]) == True :
                return HttpResponseRedirect(reverse("is_first_login"))
            else:
                return HttpResponseRedirect(reverse("login_again"))
  

def login_again(request):
    '''带有验证码的登陆视图'''

    template_var={}
    form = LoginAgainForm()   
    if request.method == 'POST':
        form=LoginAgainForm(request.POST.copy())  
        if form.is_valid():
            human = True
            if _login(request,form.cleaned_data["username"],form.cleaned_data["password"]) == True :
                return HttpResponseRedirect(reverse("is_first_login"))
            else:
                return HttpResponseRedirect(reverse("login_again"))
    template_var["form"]=form        
    return render_to_response('accounts/login_A.html',template_var,context_instance=RequestContext(request)) ##
   
      
def _login(request,username,password):
    '''登陆核心方法'''

    ret=False ##允许密码重置的标志
    user=authenticate(username=username,password=password)
    if user:
        ##coding change to login in but not actived 
        # if user.is_active:
        auth_login(request,user)
        ret=True
        # else:
        #     messages.add_message(request, messages.INFO, _(u'Your account has been disabled!'))
    else:
        #return HttpResponseRedirect(reverse("loginAgain"))
        messages.add_message(request, messages.INFO, _(u'Your username  was incorrect.'))
    return ret  ##返回密码重置的标志


def is_first_login(request):
    '''判断是否第一次登录'''

    BaseObj = Base.objects.get(user=request.user)
    if BaseObj.finish_steps :   
        return HttpResponseRedirect(reverse("to_homepage"))
    else:
        if BaseObj.identity == "D":
            return HttpResponseRedirect(reverse("dentiststep")) 
        else:
            return HttpResponseRedirect(reverse("patientstep")) 
  
        
def logout(request):
    '''注销'''
    
    auth.logout(request)
    return HttpResponseRedirect('/')

@require_http_methods(["POST"])
@csrf_exempt
def apply(request):
    try:
        data = json.loads(request.POST['data'])
        email = data['email']
        validate_email(email)
        subject = 'Apply Email'
        message = u'申请内测邮箱:' + email
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [settings.TO_EMAIL]
        send_mail(subject, message, from_email, to_email) 
        msg = "Thanks for your registering. We'll contact with you soon"
    except:
        msg = 'Verify your email address please'
    finally:
        return JsonResponse({"msg": msg})


@csrf_protect
@render_to("registration/password_change_form.html")
@login_required
def password_change(request, post_change_redirect=None, password_change_form=PasswordChangeForm):
    '''该函数是为了满足身份验证的需求，将django内部的password_change函数改写而成'''

    if post_change_redirect is None:
        post_change_redirect = reverse('auth_password_change_done')
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
        
    template_var={'form':form}

    return template_var

@render_to("registration/password_change_done.html")
def password_change_done(request):
    template_var={}
    return template_var
    
@render_to("registration/identity-choose.html")
def idchoose(request):
    template_var={}
    return template_var


def d_signup(request,backend):
    '''
    **参数**
    ``backend``
        backend是函数register所需要的，由urls.py里赋值，传入该函数
    '''
    template_var = {}
    
    # print "work as dentist"
    return register(request,backend,
                      identity="D",
                      template_name = "registration/d_signup.html",extra_context = template_var)

def p_signup(request,backend):
    template_var = {}

    # print "work as patient"
    return register(request,backend,
                      identity="P",
                      template_name = "registration/p_signup.html",extra_context = template_var) 


## OAuth Part
def _get_access_token_from_code(code):
    data = {
            "code": code,
            "client_id": '159968613525.apps.googleusercontent.com',
            "client_secret": 'bk9beZQZO3XEaQ2KEFLEACfd',
            "redirect_uri": 'http://www.identalk.com/oauth',
            "grant_type": 'authorization_code',
            }

    data = urllib.urlencode(data)
    # print data
    response = urllib2.urlopen('https://accounts.google.com/o/oauth2/token', data)
    response_str = response.read()

    access_token_group = json.loads(response_str)
    print "access_token_group: ", access_token_group
    access_token = access_token_group['access_token']

    return access_token

def _get_userinfo(code, access_token):
    response = urllib2.urlopen('https://www.googleapis.com/oauth2/v1/userinfo?access_token=' + access_token)
    userinfo_str = response.read()
    userinfo = json.loads(userinfo_str)
    print userinfo

    return userinfo

def _get_google_contacts(email, access_token):
    params = urllib.urlencode({'v': '3.0', 'alt': 'json', 'access_token': access_token})
    response = urllib2.urlopen(('https://www.google.com/m8/feeds/contacts/%s/full?' % email) + params)
    contacts_str = response.read()
    contacts = json.loads(contacts_str)
    return contacts

def _parse_contacts(contacts):
    if 'entry' in contacts['feed'] and len(contacts['feed']['entry']):
        emails = []
        contact_result = {}

        for entry in contacts['feed']['entry']:
            if u'gd$email' in entry:
                for e in entry[u'gd$email']:
                    email = e.get(u'address')
                try:
                    name = entry[u'gd$name'][u'gd$givenName'][u'$t']
                except:
                    name = email
                contact_result = {
                    "email": email,
                    "name": name
                }
                emails.append(contact_result)             

        return emails

    else:
        return None

def _email_invite(friends_emails, username):
    subject = username + ' has invited you to open an iDentalk account'
    # message = 'Join us, Please follow this link to Sign Up http://www.identalk.com/signup/p'
    message = render_to_string('registration/invite_email.txt',
                                   {'username':username})
    from_email = 'noreply@identalk.com'

    send_mail(subject, message, from_email, friends_emails)
    print "send ok"

@login_required
@render_to('accounts/invite_contacts.html')
def goo_oauth_invite_friends(request):
    code = request.GET.get('code')
    print 'Code: ', code
    access_token = _get_access_token_from_code(code)

    userinfo = _get_userinfo(code, access_token)
    useremail = userinfo['email']
    print 'Useremail: ', useremail
    contacts = _get_google_contacts(useremail, access_token)
    friends_emails = _parse_contacts(contacts)
    # print "friends_emails are: ", friends_emails

    return { "contacts": friends_emails }
    # return JsonResponse(friends_emails)

@csrf_exempt
def invite_contacts(request):
    contacts = request.POST.getlist('contacts')
    _email_invite(contacts, _show_name(request))

    return HttpResponseRedirect('/account/settings/')


def oauth_get_userinfo():
    pass

@csrf_exempt
@login_required
def manual_invite_friends(request):
    email_list = json.loads(request.POST['data'])
    friends_str = "".join(email_list['friends_emails'].split())
    friends_emails = friends_str.split(',')
    if len(friends_emails) > 1000:
        result = {
            "msg": "Your e-mail addresses is too much"
        }
    else:
        valid = False
        for i in friends_emails:
            try:
                validate_email(i)
                valid = True
            except:
                valid = False

        if valid:
            _email_invite(friends_emails, _show_name(request))
            result = {
                "msg": "Success"
            }
        else:
            result = {
                "msg": "Failed"
            }

    return JsonResponse(result)


def _get_fb_access_token_from_code(code):
    response = urllib2.urlopen('https://graph.facebook.com/oauth/access_token?client_id=617649148261434&redirect_uri=http://www.identalk.com:8000/oauth&client_secret=d4b49c62b3c9274a2767b63c8d175ae9&code=' + code)
    response_str = response.read()

    print "response str", response_str
    access_token_group = re.split('&', response_str)
    print "access_token_group: ", access_token_group
    access_token = re.split('=', access_token_group[0])[1]

    return access_token

def _get_fb_user_id(access_token):
    
    response = urllib2.urlopen('https://graph.facebook.com/me?access_token=' + access_token)
    response_str = response.read()

    fb_user_info = json.loads(response_str)
    print type(fb_user_info)
    print "fb_user_info: ", fb_user_info
    fb_user_id = fb_user_info['id']

    return fb_user_id

def _put_wall_post(request, news):
    code = request.GET.get('code')
    print code
    access_token = _get_fb_access_token_from_code(code)
    fb_user_id = _get_fb_user_id(access_token)

    data = {'access_token': access_token,
            'message': news
            }

    data = urllib.urlencode(data)
    # print data
    response = urllib2.urlopen('https://graph.facebook.com/%s/feed' % fb_user_id, data)

def fb_oauth_post_wall(request):
    news = 'Hi, I am gun, I just used python code to generate this message.'
    _put_wall_post(request, news)

    return HttpResponse('')


# ms Hotmail contacts Invite
def _get_msaccess_token_from_code(code):
    data = {
            "code": code,
            "client_id": '00000000400EDC5A',
            "client_secret": 'wnQ0lcU1q5b2-9Dvt4GC1wfabwAfnh2w',
            "redirect_uri": 'http://www.identalk.com:8000/ms/oauth',
            "grant_type": 'authorization_code',
            }

    data = urllib.urlencode(data)
    # print data
    response = urllib2.urlopen('https://login.live.com/oauth20_token.srf', data)
    response_str = response.read()

    access_token_group = json.loads(response_str)
    print type(access_token_group)
    print "access_token_group: ", access_token_group
    access_token = access_token_group['access_token']

    return access_token

def _get_msuserinfo(code, access_token):
    response = urllib2.urlopen('https://www.googleapis.com/oauth2/v1/userinfo?access_token=' + access_token)
    userinfo_str = response.read()
    userinfo = json.loads(userinfo_str)
    print userinfo

    return userinfo

def _get_hotmail_contacts(access_token):
    # params = urllib.urlencode({'v': '3.0', 'alt': 'json', 'access_token': access_token})
    response = urllib2.urlopen('https://apis.live.net/v5.0/me/contacts?access_token=' + access_token)
    contacts_str = response.read()
    # print contacts_str
    contacts = json.loads(contacts_str)
    print "contacts is: ", contacts
    return contacts["data"]

def _parse_hotcontacts(contacts):
    if len(contacts):
        emails = []
        contact_result = {}

        for entry in contacts:
            print 'entry is: ', entry
            print 'type entry:', type(entry)
            emails.append(entry['email_hashes'][0])

                ## name_unicode source look like "{u'gd$familyName': {u'$t': u'mas'}, u'gd$givenName': {u'$t': u'dubyya'}, u'gd$fullName': {u'$t': u'dubyya mas'}}"
                # name_unicode = entry[u'gd$name']
                # like = re.match("u'gd$fullName': {u'$t': u'" + (?P<name_look>.*) + "'}", name_unicode)
                # print like
                # name = like.group('name_look')
                # print name

                # contact_result.update(name=email)

        return emails

    else:
        return None

def ms_oauth_invite_friends(request):
    code = request.GET.get('code')
    print code
    access_token = _get_msaccess_token_from_code(code)

    # userinfo = _get_msuserinfo(code, access_token)
    # useremail = userinfo['email']
    # print useremail
    contacts = _get_hotmail_contacts(access_token)
    friends_emails = _parse_hotcontacts(contacts)
    print "friends_emails are: ", friends_emails

    print "email are not email format rather than sha256 hexdigest"
    _email_invite(friends_emails)

    return HttpResponse('')







# def _http_call(url, method, authorization=None, return_json=True, **kw):  
#     ''''' 
#     send an http request and return headers and body if no error. 
#     '''  
#     params = None  
#     boundary = None  
#     if method==_HTTP_UPLOAD:  
#         params, boundary = _encode_multipart(**kw)  
#     else:  
#         params = _encode_params(**kw)  
#     http_url = '%s?%s' % (url, params) if method==_HTTP_GET and params else url  
#     http_body = None if method==_HTTP_GET else params  
#     req = urllib2.Request(http_url, data=http_body)  
#     if authorization:  
#         print 'Authorization:', authorization  
#         req.add_header('Authorization', authorization)  
#     if boundary:  
#         req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)  
#     print method, http_url, 'BODY:', http_body  
#     resp = urllib2.urlopen(req)  
#     body = resp.read()  
#     if return_json:  
#         r = json.loads(body, object_hook=_obj_hook)  
#         if hasattr(r, 'error_code'):  
#             raise APIError(r.error_code, getattr(r, 'error', ''), getattr(r, 'request', ''))  
#         return r  
#     return body

# def _parse_params(params_str, unicode_value=True):  
#     d = dict()  
#     for s in params_str.split('&'):  
#         n = s.find('=')  
#         if n>0:  
#             key = s[:n]  
#             value = urllib.unquote(s[n+1:])  
#             d[key] = value.decode('utf-8') if unicode_value else value  
#     return JsonObject(**d)

# _HTTP_GET = 0  
# _HTTP_POST = 1  
# _HTTP_UPLOAD = 2
# params = _parse_params(_http_call(url, _HTTP_GET, authorization, return_json=False), False)

# def _encode_params(**kw):  
#     ''''' 
#     Encode parameters. 
#     '''  
#     if kw:  
#         args = []  
#         for k, v in kw.iteritems():  
#             qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)  
#             args.append('%s=%s' % (k, _quote(qv)))  
#         return '&'.join(args)  
#     return ''  
  
# def _quote(s):  
#     ''''' 
#     quote everything including / 
     
#     >>> _quote(123) 
#     '123' 
#     >>> _quote(u'\u4e2d\u6587') 
#     '%E4%B8%AD%E6%96%87' 
#     >>> _quote('/?abc=def& _+%') 
#     '%2F%3Fabc%3Ddef%26%20_%2B%25' 
#     '''  
#     if isinstance(s, unicode):  
#         s = s.encode('utf-8')  
#     return urllib.quote(str(s), safe='')  
  
# def _generate_nonce():  
#     ' generate random uuid as oauth_nonce '  
#     return uuid.uuid4().hex  
  
# def _generate_signature(key, base_string):  
#     ''''' 
#     generate url-encoded oauth_signature with HMAC-SHA1 
#     '''  
#     return _quote(base64.b64encode(hmac.new(key, base_string, hashlib.sha1).digest()))  
  
# def _generate_base_string(method, url, **params):  
#     ''''' 
#     generate base string for signature 
     
#     >>> method = 'GET' 
#     >>> url = 'http://www.sina.com.cn/news' 
#     >>> params = dict(a=1, b='A&B') 
#     >>> _generate_base_string(method, url, **params) 
#     'GET&http%3A%2F%2Fwww.sina.com.cn%2Fnews&a%3D1%26b%3DA%2526B' 
#     '''  
#     plist = [(_quote(k), _quote(v)) for k, v in params.iteritems()]  
#     plist.sort()  
#     return '%s&%s&%s' % (method, _quote(url), _quote('&'.join(['%s=%s' % (k, v) for k, v in plist])))  
  
# if __name__=='__main__':  
#     import doctest  
#     doctest.testmod()