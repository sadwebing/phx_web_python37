# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0013_auto_20180625_1635'),
        ('monitor', '0013_project_t_domain'),
    ]

    operations = [
        migrations.CreateModel(
            name='cdn_proj_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.IntegerField(unique=True, choices=[(0, 'fh_app'), (1, 'fh_cp_static')])),
            ],
        ),
        migrations.CreateModel(
            name='cdn_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='cdn_proj_t',
            name='cdn',
            field=models.ManyToManyField(to='monitor.cdn_t'),
        ),
        migrations.AddField(
            model_name='cdn_proj_t',
            name='domain',
            field=models.ManyToManyField(to='detect.domains'),
        ),
    ]
