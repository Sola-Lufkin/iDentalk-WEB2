#coding=utf-8
"""
URL patterns for the views included in ``django.contrib.auth``.

Including these URLs (via the ``include()`` directive) will set up the
following patterns based at whatever URL prefix they are included
under:

* User login at ``login/``.

* User logout at ``logout/``.

* The two-step password change at ``password/change/`` and
  ``password/change/done/``.

* The four-step password reset at ``password/reset/``,
  ``password/reset/confirm/``, ``password/reset/complete/`` and
  ``password/reset/done/``.

The default registration backend already has an ``include()`` for
these URLs, so under the default setup it is not necessary to manually
include these views. Other backends may or may not include them;
consult a specific backend's documentation for details.

"""

from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views

urlpatterns = patterns('',
                       url(r'^login/$',
                           accounts_views.login,
                           {'template_name': 'registration/login.html'},
                           name='auth_login'),
                       url(r'^logout/$',
                           accounts_views.logout,
                           #{'template_name': 'registration/logout.html'},
                           name='auth_logout'),
                       
                       url(r'^password/change/$',
                           accounts_views.password_change,
                           name='auth_password_change'),

                       url(r'^password/change/done/$',
                           accounts_views.password_change_done,
                           name='auth_password_change_done'),
                       
                       url(r'^password/reset/$',
                           auth_views.password_reset,
                           name='auth_password_reset'),
                       url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           auth_views.password_reset_confirm,
                           name='auth_password_reset_confirm'),
                       url(r'^password/reset/complete/$',
                           auth_views.password_reset_complete,
                           name='auth_password_reset_complete'),
                       url(r'^password/reset/done/$',
                           auth_views.password_reset_done,
                           name='auth_password_reset_done'),
                       url(r'^login/again/$',accounts_views.login_again,
                           name='login_again'),
                       url(r'^first_login$',
                           accounts_views.is_first_login,
                           name="is_first_login"),
)
