import schedule
import time
import threading
# # from django.conf import settings
# # import customusermodel.settings as app_settings
# # settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS,DATABASES=app_settings.DATABASES)
# # import django
# # django.setup()


# from __future__ import unicode_literals


import os
os.environ["DJANGO_SETTINGS_MODULE"] = "customusermodel.settings"


import django
django.setup()

from celery123 import *
from accounts.models import *
from datetime import datetime

def job():
    epoch = time.mktime(datetime.now().timetuple())
    upcomming_queue.objects.all().delete()
    # epoch = 1571790600
    for x in scheduler_model.objects.filter(timestamp__lte=int(epoch)+600,timestamp__gte=epoch):
        obj = upcomming_queue()
        obj.username = MyUser.objects.get(dirtybit = x.dirtybit)
        obj.dirtybit = x.dirtybit
        # print(type(x.init_schedule_fk.self_dirtybit),'hi')
        obj.init_schedule_fk = init_schedule.objects.filter(self_dirtybit = x.init_schedule_fk.self_dirtybit)[0]
        obj.schedule_dirtybit = scheduler_model.objects.get(schedule_dirtybit = x.schedule_dirtybit)
        obj.timestamp = x.timestamp
        obj.provider = connections.objects.get(account_uid=x.provider)
        obj.save()
        reverse.delay(x.provider.provider,x.timestamp - datetime.timestamp(datetime.now()))
    print('Running ', datetime.now())


schedule.every(3).minutes.do(job)


while True:
    schedule.run_pending()

