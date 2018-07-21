# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0023_auto_20180721_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minion_t',
            name='provider',
            field=models.IntegerField(default=1, choices=[(1, '\u53f0\u6e7e\u673a\u623f'), (2, '\u9999\u6e2f\u673a\u623f'), (3, 'fent'), (4, '\u661f\u8054'), (5, '\u4e45\u901f'), (6, '\u675c\u675c'), (7, '\u7f51\u65f6'), (8, '\u4f18\u4e0e\u4e91')]),
        ),
        migrations.AlterField(
            model_name='minion_t',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, '\u542f\u7528'), (0, '\u7981\u7528')]),
        ),
    ]
