# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0016_auto_20180626_1552'),
    ]

    operations = [
        migrations.DeleteModel(
            name='wangsu_t',
        ),
        migrations.AddField(
            model_name='cdn_t',
            name='account',
            field=models.CharField(default=datetime.datetime(2018, 6, 28, 15, 55, 8, 643000), max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cdn_t',
            name='secretid',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cdn_t',
            name='secretkey',
            field=models.CharField(default=datetime.datetime(2018, 6, 28, 15, 55, 17, 531000), max_length=128),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='cdn_t',
            unique_together=set([('name', 'account')]),
        ),
    ]
