# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tomcat_url',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minion_id', models.CharField(max_length=32, null=True)),
                ('ip_addr', models.CharField(max_length=32, null=True)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
    ]
