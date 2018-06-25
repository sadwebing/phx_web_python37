# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0012_auto_20180625_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domains',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, '\u542f\u7528'), (0, '\u7981\u7528')]),
        ),
        migrations.AlterField(
            model_name='groups',
            name='ssl',
            field=models.IntegerField(default=1, choices=[(1, '\u542f\u7528'), (0, '\u7981\u7528')]),
        ),
    ]
