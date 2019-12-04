# Creatosaurus
Creatosaurus - Scheduling Posts on Facebook(Post+ Image Post), Twitter(Tweet+ Image Tweet) and Linkedin(Post+ Image Post) using Celery and Custom Timer (Without APScheduler) in Python, Django. Using this one can schedule Posts for next 2 years, currently in Testing Mode but all operations are working fine.
Payment Gateway Integrated.
Create Custom Packages.
Queue System implemented for scheduling of posts.
Notification System also implemented.

## How To Run 
-> py manage.py runsslserver localhost:8000 --certificate server.crt --key server.key
 -> py -m celery -A celery123 worker --pool=eventlet -l info  --concurrency=100
-> py timer.py

Using Celery concurrency we are using 100 workers in parallel, which can run 100 tasks in parallel. Once the timer is started it checks for next tasks in upcomming 15mins and send a request to the celery to run at that required time, this process of finding the task is performed in every 10 mins. So in every 10 mins the timer.py searches for the tasks that are there in the next 15 mins. Once the tasks are captured they are sent to the Upcomming Queue Model(Table) from where the celery fetches the required data.
