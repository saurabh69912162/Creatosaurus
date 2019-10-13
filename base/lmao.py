from django.conf import settings
import customusermodel.settings as app_settings

settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS,DATABASES=app_settings.DATABASES)

import django
django.setup()

from accounts.models import MyUser
for s in MyUser.objects.all():
    print(s)