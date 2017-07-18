from django.db import models


class PullRequest(models.Model):
    updated_on = models.DateTimeField()
    updated_by = models.CharField(max_length=500)
    key = models.CharField(max_length=150)
    author = models.CharField(max_length=500)
    task_count = models.IntegerField()
    build_count = models.IntegerField()
    last_build = models.CharField(max_length=500, null=True)


class PullRequestApproval(models.Model):
    display_name = models.CharField(max_length=500)
    avatar = models.TextField()

    pullrequest = models.ForeignKey(PullRequest, related_name='approvals')
