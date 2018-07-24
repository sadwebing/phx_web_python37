# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0029_auto_20180724_1829'),
    ]

    operations = [
        migrations.CreateModel(
            name='project_authority_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('read', models.IntegerField(default=1, choices=[(1, '\u542f\u7528'), (0, '\u7981\u7528')])),
                ('write', models.IntegerField(default=0, choices=[(1, '\u542f\u7528'), (0, '\u7981\u7528')])),
                ('project', models.ManyToManyField(to='monitor.project_t', blank=True)),
            ],
        ),
    ]
