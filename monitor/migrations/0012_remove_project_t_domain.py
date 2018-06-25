# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0011_auto_20180625_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project_t',
            name='domain',
        ),
    ]
