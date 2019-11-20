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
    path('config-all-platforms/<str:rand_user_string>', all_post_config),
    path('select-time/post/<str:rand_user_string>', set_timer_post),
    path('reschedule/<str:rand_string>', reschedule_post),
    path('reschedule-time/<str:rand_string>', reschedule_time),
    path('configure/post/<str:data>/',post_factory),
    path('configure/',configure),
    path('my-queue/', myqueue),
    path('package/', package),
    path('my-history/', myhistory),
    path('facebook-configure/',facebookconfigure),
    url('^accounts/', include('allauth.urls')),
    path('logout/', logout_view),
    path('test_view/',test_view),
    url(r'^password/$', change_password, name='change_password'),
    url(r'^profile/edit$', edit_profile),
    path('schedule-this-month/', schedule),
    path('payment-confirmation/<str:rand_string>/<str:rand_string1>', payment_confirmation),
    path('payment-success/<str:rand_string1>', payment_success),
    path('buy-pack-<str:pack_name>', buy_pack),

    path('schedule-for-<str:month>-<int:year>/',schedule_custom_year_month, name="schedule_custom_year_month"),


    #url(r'^profile/business$', edit_business),
    #url(r'^profile/creator', edit_creator),
    url(r'^profile/details', edit_me),
    url(r'^api/v1/', userlist.as_view()),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
