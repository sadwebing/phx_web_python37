# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0005_auto_20180521_1726'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='project_t',
            unique_together=set([('product', 'project', 'envir')]),
        ),
    ]
