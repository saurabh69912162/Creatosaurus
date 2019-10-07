from django.conf.urls import url
from django.contrib import admin

from accounts.views import *


from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^profile/$', profile, name='profile'),
    url(r'^register/$', register),
    path('', login_view),
    path('logout/', logout_view),
    url(r'^password/$', change_password, name='change_password'),
    url(r'^profile/edit$', edit_profile),
    #url(r'^profile/business$', edit_business),
    #url(r'^profile/creator', edit_creator),
    url(r'^profile/details', edit_me),
    url(r'^api/v1/', userlist.as_view()),
]



urlpatterns = format_suffix_patterns(urlpatterns)