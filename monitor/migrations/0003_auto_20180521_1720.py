# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20180521_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_t',
            name='product',
            field=models.IntegerField(choices=[(0, b'pub'), (1, b'ali'), (2, b'guangda'), (3, b'leying'), (4, b'caitou'), (5, b'tiantian'), (6, b'sande'), (7, b'uc'), (8, b'9393'), (9, b'3535'), (10, b'agcai'), (11, b'wanyou'), (12, b'fh')]),
        ),
        migrations.AlterField(
            model_name='project_t',
            name='project',
            field=models.CharField(max_length=10, choices=[('caipiao', 'caipiao'), ('sport', 'sport')]),
        ),
    ]
