# from datetime import datetime
# import schedule
# import time
# import threading
# from django.conf import settings
# import customusermodel.settings as app_settings
# settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS,DATABASES=app_settings.DATABASES)
# import django
# django.setup()


import os
os.environ["DJANGO_SETTINGS_MODULE"] = "customusermodel.settings"


import django
django.setup()


from allauth.socialaccount.models import SocialAccount, SocialToken
from celery import Celery
import time
from accounts.models import *
app = Celery('celery123',broker='amqp://localhost//')



@app.task
def reverse(key,string,number):
	# localtime = time.localtime(time.time())
	# print("Local current time :", localtime)
	# time.sleep(number)
	# print('delay is :: ',number)

	sch_dbit =  scheduler_models.objects.get(scheduler_dirtybit = key)
	social_acc = SocialAccount.objects.get(uid = string)
	account_token = SocialToken.objects.get(id=social_acc.id)
	_provider = social_acc.provider
	print(_provider)
	obj = string[::-1]
	return obj



def facebook_text():
	pass


def facebook_image_text():
	pass


def linkedin_text():
	pass


def linkedin_image():
	pass


def twitter_text():
	pass


def twitter_image():
	pass
