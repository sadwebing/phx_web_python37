# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_auto_20180127_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_t',
            name='uri',
            field=models.CharField(default='/', max_length=128),
        ),
    ]
