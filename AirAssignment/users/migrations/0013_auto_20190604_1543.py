# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-06-04 13:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20190603_0330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 4, 15, 43, 52, 361230)),
        ),
        migrations.AlterUniqueTogether(
            name='assignment',
            unique_together=set([('name', 'course')]),
        ),
    ]
