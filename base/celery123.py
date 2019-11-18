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
import requests
import json
from requests_oauthlib import OAuth1
from accounts.models import *
app = Celery('celery123',broker='amqp://localhost//')



@app.task
def reverse(key,string,number):
	# localtime = time.localtime(time.time())
	# print("Local current time :", localtime)
	time.sleep(number)
	# print('delay is :: ',number)

	# sch_dbit =  scheduler_models.objects.get(scheduler_dirtybit = key)
	# social_acc = SocialAccount.objects.get(uid = string)
	# account_token = SocialToken.objects.get(id=social_acc.id)
	# _provider = social_acc.provider
	# print(_provider)
	# obj = string[::-1]


	final_token,provider,secret = parse_info(string)
	if provider == 'facebook':
		facebook_post(final_token,string,key)
	elif provider == 'twitter':
		twitter_post(final_token,secret,string,key)
	elif provider == 'linkedin':
		linkedin_post(final_token,string,key)
	else:
		pass

	return True



def parse_info(string):
	obj  = selected_accounts.objects.get(account_uid = string)
	provider = obj.provider

	if provider == 'twitter':
		final_token = obj.access_token
		secret = obj.access_token_secret
		return final_token,provider,secret
	else:
		if obj.long_token.exists():
			final_token  = obj.long_token
			secret =''
			return final_token,provider,secret
		else:
			final_token  = obj.access_token
			secret = ''
			return final_token, provider,secret



def facebook_post(final_token, string, key):
	obj = scheduler_models.objects.get(schedule_dirtybit = key)
	if obj.image.exists():
		post = obj.content
		account_id = obj.provider
		image_url_2 = 'https://localhost:8000'+obj.image.url
		post.replace(' ', '+')
		print(requests.post("https://graph.facebook.com/" + id + "/photos/?url=" + image_url_2 +"&message=" + post + "&access_token=" + final_token))
	else:
		post = obj.content
		account_id = obj.provider
		post.replace(' ', '+')
		print(requests.post(
			"https://graph.facebook.com/"+account_id+"/feed/?message=" + post + "&access_token=" + final_token))

POST_TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'
TWITTER_CONSUMER_KEY = 'bTDdpQAjKLBL1B0r259ZbIZg2'
TWITTER_CONSUMER_SECRET = 'hRVFl78PDOMmBjAbAerSM5RGWLp4Om2ni2ohtRTyOYqFZUABp7'
MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'


def twitter_post(final_token,secret, string, key):
	obj = scheduler_models.objects.get(schedule_dirtybit = key)
	if obj.image.exists():
		pass
	else:
		oauth = OAuth1(TWITTER_CONSUMER_KEY,
					   client_secret=TWITTER_CONSUMER_SECRET,
					   resource_owner_key=final_token,
					   resource_owner_secret=secret)
		request_data = {'status': obj.content, }
		req = requests.post(url=POST_TWEET_URL, data=request_data, auth=oauth)


def linkedin_post(final_token, string, key):
	obj = scheduler_models.objects.get(schedule_dirtybit = key)
	if obj.image.exists():
		user_id = string
		user_urn_id = "urn:li:person:" + user_id
		status = obj.content
		url = "https://api.linkedin.com/v2/ugcPosts"
		is_url_given = 'https://localhost:8000'+obj.image.url
		payload = "{\n    \"author\": \"" + user_urn_id + "\",\n    \"lifecycleState\": \"PUBLISHED\",\n    \"specificContent\": {\n        \"com.linkedin.ugc.ShareContent\": {\n            \"shareCommentary\": {\n                \"text\": \"" + status + "\"\n            },\n            \"shareMediaCategory\": \"ARTICLE\",\n            \"media\": [\n                {\n                    \"status\": \"READY\",\n                    \"description\": {\n                        \"text\": \"\"\n                    },\n                    \"originalUrl\": \"" + is_url_given + "\",\n                    \"title\": {\n                        \"text\": \"\"\n                    }\n                }\n            ]\n        }\n    },\n    \"visibility\": {\n        \"com.linkedin.ugc.MemberNetworkVisibility\": \"CONNECTIONS\"\n    }\n}"
		access_token = 'Bearer ' + final_token
		headers = {
			'Content-Type': "application/raw",
			'Authorization': access_token,
		}
		response = requests.request("POST", url, data=payload, headers=headers)
		print(response.text)
	else:
		user_id = string
		user_urn_id = "urn:li:person:" + user_id
		status = obj.content
		url = "https://api.linkedin.com/v2/ugcPosts"
		payload = "{\n\"author\": \"" + user_urn_id + "\",\n\"lifecycleState\":\"PUBLISHED\",\n\"specificContent\": {\n\"com.linkedin.ugc.ShareContent\": {\n\"shareCommentary\": {\n\"text\": \"" + status + "\"\n},\n\"shareMediaCategory\": \"NONE\"\n}\n},\n\"visibility\": {\n\"com.linkedin.ugc.MemberNetworkVisibility\": \"PUBLIC\"\n}\n}"

		access_token = 'Bearer ' + final_token
		headers = {
			'Content-Type': "application/raw",
			'Authorization': access_token,
		}
		response = requests.request("POST", url, data=payload, headers=headers)
		print(response.text)
