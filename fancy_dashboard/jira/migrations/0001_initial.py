# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-24 17:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JiraClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('password', models.TextField()),
                ('url', models.URLField()),
            ],
        ),
    ]
