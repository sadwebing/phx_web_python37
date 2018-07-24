# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0028_auto_20180723_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minion_t',
            name='provider',
            field=models.IntegerField(default=1, choices=[(1, '\u53f0\u6e7e\u673a\u623f'), (2, '\u9999\u6e2f\u673a\u623f'), (3, 'fent'), (4, '\u661f\u8054'), (5, '\u4e45\u901f'), (6, '\u675c\u675c'), (7, '\u7f51\u65f6'), (8, '\u4f18\u4e0e\u4e91'), (9, '\u963f\u91cc\u4e91')]),
        ),
        migrations.AlterField(
            model_name='project_t',
            name='product',
            field=models.IntegerField(choices=[(0, b'pub'), (1, b'ali'), (2, b'guangda'), (3, b'leying'), (4, b'caitou'), (5, b'tiantian'), (6, b'sande'), (7, b'uc'), (8, b'9393'), (9, b'3535'), (19, b'1717'), (10, b'agcai'), (20, b'fulicai'), (22, b'yrcai'), (23, b'yiteng'), (24, b'yonglihui'), (25, b'618cai'), (28, b'letian'), (21, b'leducheng'), (11, b'wanyou'), (13, b'le7'), (14, b'dx_6668'), (15, b'dx_70887'), (17, b'yy'), (18, b'yongfa'), (12, b'fenghuang'), (16, b'yongshi'), (27, b'ruiyin'), (26, b'java')]),
        ),
        migrations.AlterField(
            model_name='project_t',
            name='project',
            field=models.CharField(max_length=10, choices=[('caipiao', 'caipiao'), ('sport', 'sport'), ('houtai', 'houtai'), ('pay', 'pay'), ('ggz', 'ggz'), ('vpn', 'vpn'), ('image', 'image'), ('httpdns', 'httpdns')]),
        ),
    ]
