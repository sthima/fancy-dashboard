from django.db import models

from fancy_dashboard.jira.models import JiraClient


class SprintIssueAssigneeManager(models.Manager):
    def create_or_update(self, display_name, avatar, email):
        user = self.get_queryset().filter(email=email).first()
        if not user:
            user = self.model()
        user.display_name = display_name
        user.avatar = avatar
        user.email = email
        user.save()
        return user


class SprintIssueAssignee(models.Model):
    display_name = models.CharField(max_length=500)
    avatar = models.TextField()
    email = models.EmailField()

    objects = SprintIssueAssigneeManager()

    def __str__(self):
        return self.display_name


class SprintIssueTypeManager(models.Manager):
    def create_or_update(self, name, icon):
        issue_type = self.get_queryset().filter(name=name).first()
        if not issue_type:
            issue_type = self.model()
        issue_type.name = name
        issue_type.icon = icon
        issue_type.save()
        return issue_type


class SprintIssueType(models.Model):
    name = models.CharField(max_length=500, unique=True)
    icon = models.TextField()

    objects = SprintIssueTypeManager()

    def __str__(self):
        return self.name


class SprintIssue(models.Model):
    rank = models.CharField(max_length=1000)
    key = models.CharField(max_length=150, unique=True)

    url = models.TextField()
    assignee = models.ForeignKey(SprintIssueAssignee, related_name='issues', null=True)
    # issue_type = models.CharField(max_length=50)
    issue_type = models.ForeignKey(SprintIssueType, related_name='issues', null=True)
    project = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
    # version = models.CharField(max_length=20)

    client = models.ForeignKey(JiraClient, related_name='current_sprint')

    def __str__(self):
        return self.key
