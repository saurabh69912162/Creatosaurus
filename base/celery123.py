# from datetime import datetime
# import schedule
# import time
# import threading
# from django.conf import settings
# import customusermodel.settings as app_settings
# settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS,DATABASES=app_settings.DATABASES)
# import django
# django.setup()


from __future__ import unicode_literals

import os
os.environ["DJANGO_SETTINGS_MODULE"] = "customusermodel.settings"

from celery import Celery
import time
from models import *
app = Celery('celery123',broker='amqp://localhost//')



@app.task
def reverse(string,number):
	localtime = time.localtime(time.time())
	print("Local current time :", localtime)
	print('delay is :: ',number)
	obj = string[::-1]
	return obj

