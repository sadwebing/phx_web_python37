# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0021_auto_20180721_1854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='minion_t',
            name='password',
        ),
        migrations.RemoveField(
            model_name='minion_t',
            name='port',
        ),
        migrations.AddField(
            model_name='project_t',
            name='password',
            field=models.CharField(default='/', max_length=128),
        ),
        migrations.AddField(
            model_name='project_t',
            name='port',
            field=models.IntegerField(default=11223),
        ),
    ]
