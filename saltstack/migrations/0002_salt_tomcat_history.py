# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('saltstack', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='salt_tomcat_history',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('op_time', models.CharField(max_length=128)),
                ('op_user', models.CharField(max_length=20)),
                ('op_ip_addr', models.GenericIPAddressField()),
                ('op_type', models.CharField(max_length=64)),
                ('op_before', models.CharField(max_length=2048)),
                ('op_after', models.CharField(max_length=2048)),
            ],
        ),
    ]
