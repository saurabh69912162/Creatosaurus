from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from accounts.views import *
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^profile/$', profile, name='profile'),
    url(r'^register/$', register),
    path('', login_view),
    path('connect/',connect),
    path('configure/',configure),
    # path('lol/',lol),
    path('facebook-configure/',facebookconfigure),
    url('^accounts/', include('allauth.urls')),
    path('logout/', logout_view),
    url(r'^password/$', change_password, name='change_password'),
    url(r'^profile/edit$', edit_profile),
    #url(r'^profile/business$', edit_business),
    #url(r'^profile/creator', edit_creator),
    url(r'^profile/details', edit_me),
    url(r'^api/v1/', userlist.as_view()),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
