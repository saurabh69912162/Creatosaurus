# from datetime import datetime
# import schedule
# import time
# import threading
# from django.conf import settings
# import customusermodel.settings as app_settings
# settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS,DATABASES=app_settings.DATABASES)
# import django
# django.setup()
# >py -m celery -A celery123 worker --pool=eventlet -l info  --concurrency=100
# py -m celery -A celery123 worker --pool=eventlet -l info

import os

os.environ["DJANGO_SETTINGS_MODULE"] = "customusermodel.settings"

import django

django.setup()

from allauth.socialaccount.models import SocialAccount, SocialToken
from celery import Celery
import time
import sys
import requests
import json
from requests_oauthlib import OAuth1
from accounts.models import *
app = Celery('celery123', broker='amqp://localhost//')


@app.task
def reverse(key, string, number):
    print('key is ',key)
    print('string is ',string)
    # localtime = time.localtime(time.time())
    # print("Local current time :", localtime)
    # time.sleep(number)
    print('tried sleeping for ',number,' seconds')
    # print('delay is :: ',number)
    # sch_dbit =  scheduler_models.objects.get(scheduler_dirtybit = key)
    # social_acc = SocialAccount.objects.get(uid = string)
    # account_token = SocialToken.objects.get(id=social_acc.id)
    # _provider = social_acc.provider
    # print(_provider)
    # obj = string[::-1]
    final_token, provider, secret = parse_info(string)
    if provider == 'facebook':
        # time.sleep(10)
        facebook_post(final_token, string, key)
    elif provider == 'twitter':
        twitter_post(final_token, secret, string, key)
    elif provider == 'linkedin':
        linkedin_post(final_token, string, key)
    else:
        pass
    return key

from accounts.models import *

def parse_info(string):
    print('i am finding :: ',string)
    obj = selected_connections.objects.get(account_uid=string)
    provider = obj.provider
    print(provider)

    if provider == 'twitter':
        final_token = str(obj.access_token)
        secret = obj.access_token_secret
        return final_token, provider, secret
    else:
        if obj.long_token:
            final_token = obj.long_token
            print('Final Access Token :',final_token)
            print('Final Token Type : ',type(final_token))
            secret = ''
            return final_token, provider, secret
        else:
            final_token = obj.access_token
            print('Final Access Token :', final_token)
            print('Final Token Type : ', type(final_token))
            secret = ''
            return final_token, provider, secret


def facebook_post(final_token, string, key):
    obj = scheduler_model.objects.get(schedule_dirtybit=key)
    if obj.image:
        post = obj.content
        account_id = str(obj.provider)
        # image_url_2 = 'https://localhost:8000' + obj.image.url
        image_url_2 = 'https://cdn.pixabay.com/photo/2019/11/04/17/30/happy-4601691_1280.jpg'
        post1 = post.replace(' ', '+')
        print('Posting')
        print(requests.post("https://graph.facebook.com/" + account_id + "/photos/?url=" + image_url_2 + "&message="+post1+"&access_token=" + final_token))
        obj.hit = True
        obj.save()
    else:
        post = obj.content
        account_id = str(obj.provider)
        print('Posting')
        post1 = post.replace(' ', '+')
        print(requests.post("https://graph.facebook.com/"+account_id+"/feed/?message="+post1+"&access_token="+final_token))
        obj.hit = True
        obj.save()


TWITTER_CONSUMER_KEY = 'xxxxxxxxxxxxxxxxxxxx'
TWITTER_CONSUMER_SECRET = 'xxxxxxxxxxxxxxxxxxxxx'
MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'
POST_TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'


class imageTweet(object):
    def __init__(self, file_name, abc):
        oauth = abc
        self.video_filename = file_name
        self.total_bytes = os.path.getsize(self.video_filename)
        self.media_id = None
        self.processing_info = None

    def upload_init(self, abc):
        '''
        Initializes Upload
        '''
        print('INIT')

        request_data = {
            'command': 'INIT',
            'media_type': 'image/jpeg',
            'total_bytes': self.total_bytes,

        }
        oauth = abc
        req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)
        print(req.text)
        m_id = req.json()
        media_id = m_id['media_id']

        self.media_id = media_id

        print('Media ID: %s' % str(media_id))

    def upload_append(self, abc):
        '''
        Uploads media in chunks and appends to chunks uploaded
        '''
        oauth = abc
        segment_id = 0
        bytes_sent = 0
        file = open(self.video_filename, 'rb')

        while bytes_sent < self.total_bytes:
            chunk = file.read(4 * 1024 * 1024)

            print('APPEND')

            request_data = {
                'command': 'APPEND',
                'media_id': self.media_id,
                'segment_index': segment_id
            }
            files = {
                'media': chunk
            }

            req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, files=files, auth=oauth)

            if req.status_code < 200 or req.status_code > 299:
                print(req.status_code)
                print(req.text)
                sys.exit(0)

            segment_id = segment_id + 1
            bytes_sent = file.tell()
            print('%s of %s bytes uploaded' % (str(bytes_sent), str(self.total_bytes)))
        print('Upload chunks complete.')


    def upload_finalize(self, abc):
        oauth = abc
        print('FINALIZE')
        request_data = {
            'command': 'FINALIZE',
            'media_id': self.media_id
        }
        req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)
        print(req.json())
        print('FINALIZE done')
        self.processing_info = req.json().get('processing_info', None)
        self.check_status(abc)

    def check_status(self, abc):
        oauth = abc
        if self.processing_info is None:
            return
        state = self.processing_info['state']
        print('Media processing status is %s ' % state)
        if state == u'succeeded':
            return
        if state == u'failed':
            sys.exit(0)
        check_after_secs = self.processing_info['check_after_secs']
        print('Checking after %s seconds' % str(check_after_secs))
        time.sleep(check_after_secs)
        print('STATUS')
        request_params = {
            'command': 'STATUS',
            'media_id': self.media_id
        }
        req = requests.get(url=MEDIA_ENDPOINT_URL, params=request_params, auth=oauth)
        self.processing_info = req.json().get('processing_info', None)
        self.check_status()

    def tweet(self, abc, status):
        oauth = abc
        request_data = {
            'status': status,
            'media_ids': self.media_id
        }
        req = requests.post(url=POST_TWEET_URL, data=request_data, auth=oauth)
        # print(req.json())


def twitter_post(final_token, secret, string, key):
    obj = scheduler_model.objects.get(schedule_dirtybit=key)
    if obj.image:

        CONSUMER_KEY = 'xxxxxxxxxxxxxxxxxxxx'
        CONSUMER_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        ACCESS_TOKEN = final_token
        ACCESS_TOKEN_SECRET = secret
        # VIDEO_FILENAME = "E:\Creatosaurus-in\ backend\Creatosaurus\ base\ accounts\media" + obj.image.url  # might have to give local file address rather than url
        name = obj.image.url
        file_name = name.replace('/', '\\')
        VIDEO_FILENAME = "E:\\Creatosaurus-in\\backend\\Creatosaurus\\base\\accounts" + file_name
        print(VIDEO_FILENAME)
        # VIDEO_FILENAME = 'https://cdn.pixabay.com/photo/2019/11/04/17/30/happy-4601691_1280.jpg'
        oauth = OAuth1(TWITTER_CONSUMER_KEY,
                       client_secret=TWITTER_CONSUMER_SECRET,
                       resource_owner_key=final_token,
                       resource_owner_secret=str(secret))

        imageTwi = imageTweet(VIDEO_FILENAME, oauth)
        imageTwi.upload_init(oauth)
        imageTwi.upload_append(oauth)
        imageTwi.upload_finalize(oauth)
        imageTwi.tweet(oauth, obj.content)
        obj.hit = True
        obj.save()


    else:
        print('Final Token ::',final_token,type(final_token))
        print('Final Secret ::',str(secret),type(secret))

        oauth = OAuth1(TWITTER_CONSUMER_KEY,
                       client_secret=TWITTER_CONSUMER_SECRET,
                       resource_owner_key=final_token,
                       resource_owner_secret=str(secret))
        request_data = {'status': str(obj.content), }
        req = requests.post(url=POST_TWEET_URL, data=request_data, auth=oauth)
        print(req.text)
        print('conetnt was ',str(obj.content),type(obj.content))
        obj.hit = True
        obj.save()

def linkedin_post(final_token, string, key):
    obj = scheduler_model.objects.get(schedule_dirtybit=key)
    if obj.image:
        user_id = string
        user_urn_id = "urn:li:person:" + user_id
        status = str(obj.content)
        url = "https://api.linkedin.com/v2/ugcPosts"
        # is_url_given = 'https://localhost:8000' + obj.image.url
        is_url_given = "https://cdn.pixabay.com/photo/2019/11/04/17/30/happy-4601691_1280.jpg"
        payload = "{\n    \"author\": \"" + user_urn_id + "\",\n    \"lifecycleState\": \"PUBLISHED\",\n    \"specificContent\": {\n        \"com.linkedin.ugc.ShareContent\": {\n            \"shareCommentary\": {\n                \"text\": \"" + status + "\"\n            },\n            \"shareMediaCategory\": \"ARTICLE\",\n            \"media\": [\n                {\n                    \"status\": \"READY\",\n                    \"description\": {\n                        \"text\": \"\"\n                    },\n                    \"originalUrl\": \"" + is_url_given + "\",\n                    \"title\": {\n                        \"text\": \"\"\n                    }\n                }\n            ]\n        }\n    },\n    \"visibility\": {\n        \"com.linkedin.ugc.MemberNetworkVisibility\": \"CONNECTIONS\"\n    }\n}"
        access_token = 'Bearer ' + str(final_token)
        headers = {
            'Content-Type': "application/raw",
            'Authorization': access_token,
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)
        obj.hit = True
        obj.save()
    else:
        user_id = string
        user_urn_id = "urn:li:person:" + user_id
        status = str(obj.content)
        url = "https://api.linkedin.com/v2/ugcPosts"
        payload = "{\n\"author\": \"" + user_urn_id + "\",\n\"lifecycleState\":\"PUBLISHED\",\n\"specificContent\": {\n\"com.linkedin.ugc.ShareContent\": {\n\"shareCommentary\": {\n\"text\": \"" + status + "\"\n},\n\"shareMediaCategory\": \"NONE\"\n}\n},\n\"visibility\": {\n\"com.linkedin.ugc.MemberNetworkVisibility\": \"PUBLIC\"\n}\n}"
        access_token = 'Bearer ' + str(final_token)
        headers = {
            'Content-Type': "application/raw",
            'Authorization': access_token,
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)
        obj.hit = True
        obj.save()
