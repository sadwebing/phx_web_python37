# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_auto_20180521_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_t',
            name='info',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='project_t',
            name='project',
            field=models.CharField(max_length=10, choices=[('caipiao', 'caipiao'), ('sport', 'sport'), ('cp_ht', 'cp_ht')]),
        ),
    ]
