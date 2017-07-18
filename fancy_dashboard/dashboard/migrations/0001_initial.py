# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-18 20:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                ('pullrequest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pullrequests', to='bitbucket.BitbucketClient')),
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
    ]
