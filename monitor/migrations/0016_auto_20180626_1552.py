# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0015_auto_20180625_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='wangsu_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64)),
                ('apikey', models.CharField(max_length=128)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='wangsu_t',
            unique_together=set([('username', 'apikey')]),
        ),
    ]
