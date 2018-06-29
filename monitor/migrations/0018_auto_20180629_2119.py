# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0017_auto_20180628_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cdn_proj_t',
            name='cdn',
        ),
        migrations.RemoveField(
            model_name='project_t',
            name='domain',
        ),
        migrations.AlterField(
            model_name='cdn_proj_t',
            name='project',
            field=models.IntegerField(unique=True, choices=[(0, 'fh_app'), (1, 'fh_cp_static'), (2, 'ry_sp_static')]),
        ),
        migrations.AlterField(
            model_name='project_t',
            name='product',
            field=models.IntegerField(choices=[(0, b'pub'), (1, b'ali'), (2, b'guangda'), (3, b'leying'), (4, b'caitou'), (5, b'tiantian'), (6, b'sande'), (7, b'uc'), (8, b'9393'), (9, b'3535'), (19, b'1717'), (10, b'agcai'), (20, b'fulicai'), (22, b'yrcai'), (23, b'yiteng'), (24, b'yonglihui'), (25, b'618cai'), (21, b'leducheng'), (11, b'wanyou'), (13, b'le7'), (14, b'dx_6668'), (15, b'dx_70887'), (17, b'yy'), (18, b'yongfa'), (12, b'fenghuang'), (16, b'yongshi'), (27, b'ruiying'), (26, b'java')]),
        ),
    ]
