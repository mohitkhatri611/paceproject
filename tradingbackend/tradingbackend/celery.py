from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
#from celery.schedules import crontab
#crontab is required to schedule task at specific time

"""most of settings remain same for celery here"""
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tradex.settings')

app = Celery('tradex')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

#celery beat settings to schedule the task
app.conf.beat_schedule = {
    #commented because we want dynamic and task should be called only when user is there on website
    #then only we call celery to call 3rd party api
    #we want dynamic schedule
    # 'every-10-seconds' : {
    #     'task': 'mainapp.tasks.update_stock2',
    #     'schedule': 10,
    #     'args': (['RELIANCE.NS', 'BAJAJFINSV.NS'],)
    # },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')