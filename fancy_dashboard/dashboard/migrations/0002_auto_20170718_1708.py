# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-18 20:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pullrequest',
            old_name='pullrequest',
            new_name='client',
        ),
    ]