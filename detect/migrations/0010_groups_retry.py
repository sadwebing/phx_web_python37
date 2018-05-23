# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0009_auto_20180521_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='retry',
            field=models.IntegerField(default=3),
        ),
    ]
