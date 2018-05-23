# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0008_auto_20180522_1854'),
    ]

    operations = [
        migrations.CreateModel(
            name='telegram_user_id_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('user_id', models.IntegerField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='telegram_user_id_t',
            unique_together=set([('user', 'user_id')]),
        ),
    ]
