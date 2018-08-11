# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20180811_1820'),
        ('monitor', '0053_project_group_authority_t'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project_group_authority_t',
            name='permission',
        ),
        migrations.RemoveField(
            model_name='project_group_authority_t',
            name='project',
        ),
        migrations.DeleteModel(
            name='project_group_authority_t',
        ),
    ]
