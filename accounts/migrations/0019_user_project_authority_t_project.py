# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0055_minion_t_system'),
        ('accounts', '0018_auto_20180812_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_project_authority_t',
            name='project',
            field=models.ManyToManyField(to='monitor.project_t'),
        ),
    ]
