# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0032_auto_20180725_1715'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='project_t',
            unique_together=set([('product', 'project', 'envir')]),
        ),
        migrations.RemoveField(
            model_name='project_t',
            name='server_type',
        ),
    ]
