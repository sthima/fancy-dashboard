from django.db import models

from fancy_dashboard.jira.models import JiraClient


class Release(models.Model):
    class Meta:
        unique_together = ('project', 'version',)
    project = models.CharField(max_length=150)
    version = models.CharField(max_length=20)

    client = models.ForeignKey(JiraClient, related_name='next_releases')

    def __str__(self):
        return "%s - %s" % (self.project, self.version)


class ReleaseStatus(models.Model):
    release = models.ForeignKey(Release, related_name='statuses')
    status = models.CharField(max_length=150)
    style = models.CharField(max_length=150)
    count = models.IntegerField()
