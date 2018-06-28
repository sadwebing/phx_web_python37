# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0014_auto_20180625_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cdn_t',
            name='name',
            field=models.IntegerField(choices=[(0, 'tencent'), (1, 'wangsu')]),
        ),
    ]
