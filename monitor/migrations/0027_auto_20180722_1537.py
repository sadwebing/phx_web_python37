# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0026_auto_20180721_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='minion_t',
            name='password',
            field=models.TextField(default='/'),
        ),
        migrations.AddField(
            model_name='minion_t',
            name='port',
            field=models.IntegerField(default=11223),
        ),
        migrations.AddField(
            model_name='minion_t',
            name='user',
            field=models.CharField(default='root', max_length=24),
        ),
    ]
