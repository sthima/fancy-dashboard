# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from fancy_dashboard.bitbucket.models.client import BitbucketClient
from .utils import get_pullrequests


@shared_task
def load_pullrequests():
    for client in BitbucketClient.objects.all():
        get_pullrequests(
            client,
        )
