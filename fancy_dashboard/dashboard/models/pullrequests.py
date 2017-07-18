from django.db import models

from fancy_dashboard.bitbucket.models.client import BitbucketClient


class PullRequest(models.Model):
    key = models.CharField(max_length=150, unique=True)
    updated_on = models.DateTimeField()
    updated_by = models.CharField(max_length=500)
    author = models.CharField(max_length=500)
    task_count = models.IntegerField()
    build_count = models.IntegerField()
    last_build = models.CharField(max_length=500, null=True)

    client = models.ForeignKey(BitbucketClient, related_name='pullrequests')

    def __str__(self):
        return self.key


class PullRequestApproval(models.Model):
    display_name = models.CharField(max_length=500)
    avatar = models.TextField()

    pullrequest = models.ForeignKey(PullRequest, related_name='approvals')

    def __str__(self):
        return "{} - {}".format(self.pullrequest.key, self.display_name)
