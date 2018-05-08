# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dns', '0007_auto_20180224_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='alter_history',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.CharField(max_length=32)),
                ('req_ip', models.CharField(max_length=128)),
                ('user', models.CharField(max_length=32)),
                ('pre_rec', models.CharField(max_length=256)),
                ('now_rec', models.CharField(max_length=256)),
            ],
        ),
    ]
