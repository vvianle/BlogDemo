# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-02-10 01:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20170209_1714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='has_working_schedule',
        ),
        migrations.AddField(
            model_name='myuser',
            name='is_author',
            field=models.BooleanField(default=False),
        ),
    ]
