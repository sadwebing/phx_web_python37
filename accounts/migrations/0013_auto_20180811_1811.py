# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0053_project_group_authority_t'),
        ('accounts', '0012_user_project_group_authority_t'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_project_group_authority_t',
            name='permission',
        ),
        migrations.RemoveField(
            model_name='user_project_group_authority_t',
            name='project',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='project_group',
            field=models.ManyToManyField(to='monitor.project_group_authority_t', blank=True),
        ),
        migrations.DeleteModel(
            name='user_project_group_authority_t',
        ),
    ]
