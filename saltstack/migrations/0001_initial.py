# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tomcat_project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('op_time', models.CharField(max_length=20)),
                ('op_user', models.CharField(max_length=20)),
                ('op_salt_type', models.CharField(max_length=10)),
                ('op_jid', models.CharField(max_length=20)),
            ],
        ),
    ]
