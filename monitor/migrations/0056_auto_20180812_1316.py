# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0055_minion_t_system'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='project_t',
            unique_together=set([('product', 'project', 'envir', 'customer', 'server_type')]),
        ),
    ]
