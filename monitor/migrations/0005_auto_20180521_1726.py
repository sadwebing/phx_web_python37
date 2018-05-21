# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0004_auto_20180521_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_t',
            name='info',
            field=models.CharField(max_length=128, blank=True),
        ),
    ]
