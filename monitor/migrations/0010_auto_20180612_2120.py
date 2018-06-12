# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0009_auto_20180523_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_t',
            name='product',
            field=models.IntegerField(choices=[(0, b'pub'), (1, b'ali'), (2, b'guangda'), (3, b'leying'), (4, b'caitou'), (5, b'tiantian'), (6, b'sande'), (7, b'uc'), (8, b'9393'), (9, b'3535'), (10, b'agcai'), (11, b'wanyou'), (12, b'fenghuang'), (13, b'le7'), (14, b'dx_6668'), (15, b'dx_70887'), (16, b'yongshi')]),
        ),
        migrations.AlterField(
            model_name='project_t',
            name='project',
            field=models.CharField(max_length=10, choices=[('caipiao', 'caipiao'), ('sport', 'sport'), ('houtai', 'houtai'), ('vpn', 'vpn')]),
        ),
    ]
