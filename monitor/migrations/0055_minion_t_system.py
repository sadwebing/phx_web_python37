# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0054_auto_20180811_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='minion_t',
            name='system',
            field=models.CharField(default='linux', max_length=32),
        ),
    ]
