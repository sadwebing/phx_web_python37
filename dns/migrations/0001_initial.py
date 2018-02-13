# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cf_account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, null=True)),
                ('email', models.CharField(max_length=128, null=True)),
                ('key', models.CharField(max_length=128, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='cf_account',
            unique_together=set([('name', 'email')]),
        ),
    ]
