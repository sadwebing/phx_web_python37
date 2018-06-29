# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_manage'),
    ]

    operations = [
        migrations.CreateModel(
            name='cdn_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.IntegerField(choices=[(0, b'tencent'), (1, b'wangsu')])),
                ('account', models.CharField(max_length=64)),
                ('secretid', models.CharField(max_length=128)),
                ('secretkey', models.CharField(max_length=128)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='cdn_t',
            unique_together=set([('name', 'account')]),
        ),
    ]
