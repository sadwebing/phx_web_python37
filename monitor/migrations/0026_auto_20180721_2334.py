# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0025_project_t_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_t',
            name='password',
            field=models.TextField(default='/'),
        ),
    ]
