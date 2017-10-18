from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fancy_dashboard.settings.development')

app = Celery('fancy_dashboard')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# This shouldn't be here
app.conf.update(
    beat_max_loop_interval = 10,
    beat_schedule = {
        # crontab(hour=0, minute=0, day_of_week='saturday')
        'pullrequest-fetcher': {  # example: 'file-backup'
            'task': 'fancy_dashboard.dashboard.tasks.load_pullrequests',  # example: 'files.tasks.cleanup'
            'schedule': crontab(minute='*/4')
        },
        'release-fetcher': {  # example: 'file-backup'
            'task': 'fancy_dashboard.dashboard.tasks.load_releases',  # example: 'files.tasks.cleanup'
            'schedule': crontab(minute='*/10')
        },
        'sprint-fetcher': {  # example: 'file-backup'
            'task': 'fancy_dashboard.dashboard.tasks.load_sprint_issues',  # example: 'files.tasks.cleanup'
            'schedule': crontab(minute='*/1')
        },
    }
)
# app.config_from_object('django.conf:settings', namespace=['CELERY', 'CELERYBEAT'])
# app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
