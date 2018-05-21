# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0007_auto_20180516_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domains',
            name='product',
            field=models.IntegerField(choices=[(0, b'pub'), (1, b'ali'), (2, b'guangda'), (3, b'leying'), (4, b'caitou'), (5, b'tiantian'), (6, b'sande'), (7, b'uc'), (8, b'9393'), (9, b'3535'), (10, b'agcai'), (11, b'wanyou')]),
        ),
        migrations.AlterField(
            model_name='domains',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, b'\xe5\x90\xaf\xe7\x94\xa8'), (0, b'\xe7\xa6\x81\xe7\x94\xa8')]),
        ),
        migrations.AlterField(
            model_name='groups',
            name='ssl',
            field=models.IntegerField(default=1, choices=[(1, b'\xe5\x90\xaf\xe7\x94\xa8'), (0, b'\xe7\xa6\x81\xe7\x94\xa8')]),
        ),
    ]
