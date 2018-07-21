# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0020_auto_20180718_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='minion_t',
            name='info',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='minion_t',
            name='password',
            field=models.CharField(default='/', max_length=128),
        ),
        migrations.AddField(
            model_name='minion_t',
            name='port',
            field=models.IntegerField(default=11223),
        ),
        migrations.AddField(
            model_name='minion_t',
            name='price',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='minion_t',
            name='provider',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='project_t',
            name='privatekey',
            field=models.TextField(default='thisisdefaultprivatekey'),
        ),
        migrations.AddField(
            model_name='project_t',
            name='publickey',
            field=models.TextField(default='thisisdefaultpublickey'),
        ),
    ]
