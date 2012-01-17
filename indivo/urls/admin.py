from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',
    
    (r'^login/', MethodDispatcher({'GET': login, 'POST': login,}), {}, 'login-view'),
    (r'^$', MethodDispatcher({'GET': admin_show})),
    (r'^logout/', MethodDispatcher({'GET': logout})),
    (r'^record/$', MethodDispatcher({'POST': admin_record_create, 'GET': admin_record_form})),
    (r'^record/(?P<record_id>[^/]+)/$', MethodDispatcher({'GET': admin_record_show})),
    (r'^record/(?P<record_id>[^/]+)/share$', MethodDispatcher({'GET': admin_record_share_form, 'POST': admin_record_share_add})),
    (r'^record/(?P<record_id>[^/]+)/share/(?P<account_id>[^/]+)/$', MethodDispatcher({'POST': admin_record_account_share_add})),
    (r'^record/(?P<record_id>[^/]+)/owner$', MethodDispatcher({'GET': admin_record_owner_form, 'POST': admin_record_owner})),
    (r'^record/search$', MethodDispatcher({'GET': admin_record_search})),
    )
