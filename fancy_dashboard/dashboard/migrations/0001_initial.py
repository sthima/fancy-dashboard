# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-24 17:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jira', '0001_initial'),
        ('bitbucket', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PullRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=150, unique=True)),
                ('updated_on', models.DateTimeField()),
                ('updated_by', models.CharField(max_length=500)),
                ('author', models.CharField(max_length=500)),
                ('task_count', models.IntegerField()),
                ('build_count', models.IntegerField()),
                ('last_build', models.CharField(max_length=500, null=True)),
                ('url', models.TextField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pullrequests', to='bitbucket.BaseClient')),
            ],
        ),
        migrations.CreateModel(
            name='PullRequestApproval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=500)),
                ('avatar', models.TextField()),
                ('pullrequest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approvals', to='dashboard.PullRequest')),
            ],
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(max_length=150)),
                ('version', models.CharField(max_length=20)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='next_releases', to='jira.JiraClient')),
            ],
        ),
        migrations.CreateModel(
            name='ReleaseStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=150)),
                ('style', models.CharField(max_length=150)),
                ('count', models.IntegerField()),
                ('release', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='dashboard.Release')),
            ],
        ),
        migrations.CreateModel(
            name='SprintIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.CharField(max_length=1000)),
                ('key', models.CharField(max_length=150, unique=True)),
                ('url', models.TextField()),
                ('project', models.CharField(max_length=150)),
                ('status', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='SprintIssueAssignee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=500)),
                ('avatar', models.TextField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='SprintIssueType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, unique=True)),
                ('icon', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='sprintissue',
            name='assignee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='dashboard.SprintIssueAssignee'),
        ),
        migrations.AddField(
            model_name='sprintissue',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_sprint', to='jira.JiraClient'),
        ),
        migrations.AddField(
            model_name='sprintissue',
            name='issue_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='dashboard.SprintIssueType'),
        ),
        migrations.AlterUniqueTogether(
            name='release',
            unique_together=set([('project', 'version')]),
        ),
    ]
