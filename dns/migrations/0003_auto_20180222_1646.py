# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dns', '0002_auto_20180208_1704'),
    ]

    operations = [
        migrations.CreateModel(
            name='domain_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(max_length=128)),
                ('route', models.CharField(max_length=32)),
                ('cf_account_name', models.CharField(max_length=32)),
                ('zone_id', models.CharField(max_length=256)),
                ('record_id', models.CharField(max_length=256)),
                ('content', models.CharField(unique=True, max_length=128)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='domain_info',
            unique_together=set([('domain', 'route')]),
        ),
    ]
