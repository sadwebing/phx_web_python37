# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0055_minion_t_system'),
        ('accounts', '0017_auto_20180812_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_project_authority_t',
            name='project',
            field=models.ManyToManyField(to='monitor.project_t'),
        ),
        migrations.AlterField(
            model_name='user_project_authority_t',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='user_project_authority_t',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='user_project_authority_t',
            name='project',
        ),
    ]
