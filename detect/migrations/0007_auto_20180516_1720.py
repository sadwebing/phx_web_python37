# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0006_auto_20180516_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domains',
            name='product',
            field=models.IntegerField(choices=[(1, b'ali'), (2, b'guangda'), (3, b'leying'), (4, b'caitou'), (5, b'tiantian'), (6, b'sande'), (7, b'uc'), (8, b'9393'), (9, b'3535'), (10, b'agcai'), (11, b'wanyou')]),
        ),
    ]
