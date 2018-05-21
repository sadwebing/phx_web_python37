# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='minion_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minion_id', models.CharField(unique=True, max_length=32)),
                ('status', models.IntegerField(default=1, choices=[(1, '\u542f\u7528'), (0, '\u7981\u7528')])),
            ],
        ),
        migrations.AlterField(
            model_name='project_t',
            name='minion_id',
            field=models.ManyToManyField(to='monitor.minion_t'),
        ),
    ]
