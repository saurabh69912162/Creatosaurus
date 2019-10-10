from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
executors = {
    'default': ThreadPoolExecutor(90),   # max threads: 90
    'processpool': ProcessPoolExecutor(20)  # max processes 20
            }
scheduler = BackgroundScheduler(executors=executors)
scheduler.add_jobstore(DjangoJobStore(), "default")

from datetime import datetime



def timed_job():
    print('This job is run every 2 seconds.')


print(scheduler.add_job(timed_job, 'date',run_date=datetime(2019, 10, 10, 13, 20, 5)))
print(scheduler.start())




# import os
# import psutil
#
# def pro_time():
# 	for x in range(2):
# 		print(x, time.time())
# 		print(psutil.cpu_percent(percpu=True))
# 		time.sleep(1)
#
#
#
# process = psutil.Process(pro_time())
# print(process.memory_info().rss)
# print(process.memory_info()[0])
# print(process.memory_info())