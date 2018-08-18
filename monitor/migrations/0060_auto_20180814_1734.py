# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0059_auto_20180814_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='minion_ip_t',
            name='alive',
            field=models.IntegerField(default=1, choices=[(1, '\u542f\u7528'), (0, '\u7981\u7528')]),
        ),
        migrations.AddField(
            model_name='minion_t',
            name='alive',
            field=models.IntegerField(default=1, choices=[(1, '\u542f\u7528'), (0, '\u7981\u7528')]),
        ),
    ]
