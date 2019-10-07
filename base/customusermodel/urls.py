from django.conf.urls import url
from django.contrib import admin

from accounts.views import register, login_view, profile, \
    change_password, edit_profile,edit_business,userlist,edit_creator, \
    edit_me


from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from allauth.account.views import login as all_login


urlpatterns = [

    url(r'^profile/$', profile, name='profile'),
    path('', include('allauth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', register),
    path('', login_view),
    url(r'^password/$', change_password, name='change_password'),
    url(r'^profile/edit$', edit_profile),
    #url(r'^profile/business$', edit_business),
    #url(r'^profile/creator', edit_creator),
    url(r'^profile/details', edit_me),
    url(r'^api/v1/', userlist.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)