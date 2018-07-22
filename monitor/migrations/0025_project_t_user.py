# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0024_auto_20180721_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_t',
            name='user',
            field=models.CharField(default='root', max_length=24),
        ),
    ]
