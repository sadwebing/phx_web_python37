# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0002_auto_20180516_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domains',
            name='content',
            field=models.CharField(max_length=128, blank=True),
        ),
    ]
