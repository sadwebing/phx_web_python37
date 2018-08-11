# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0052_auto_20180811_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='project_group_authority_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('permission', models.ManyToManyField(to='monitor.permission_t')),
                ('project', models.ManyToManyField(to='monitor.project_t')),
            ],
        ),
    ]
