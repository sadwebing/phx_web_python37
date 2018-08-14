# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0058_auto_20180813_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project_t',
            name='uri',
        ),
        migrations.AddField(
            model_name='project_t',
            name='url',
            field=models.CharField(default='https://arno.com', max_length=128),
        ),
    ]
