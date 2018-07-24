# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0015_auto_20180718_1958'),
    ]

    operations = [
        migrations.CreateModel(
            name='cdn_account_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.IntegerField(choices=[(0, b'tencent'), (1, b'wangsu')])),
                ('account', models.CharField(max_length=64)),
                ('secretid', models.CharField(max_length=128)),
                ('secretkey', models.CharField(max_length=128)),
            ],
        ),
        migrations.AlterField(
            model_name='domains',
            name='product',
            field=models.IntegerField(choices=[(0, b'pub'), (1, b'ali'), (2, b'guangda'), (3, b'leying'), (4, b'caitou'), (5, b'tiantian'), (6, b'sande'), (7, b'uc'), (8, b'9393'), (9, b'3535'), (19, b'1717'), (10, b'agcai'), (20, b'fulicai'), (22, b'yrcai'), (23, b'yiteng'), (24, b'yonglihui'), (25, b'618cai'), (28, b'letian'), (21, b'leducheng'), (11, b'wanyou'), (13, b'le7'), (14, b'dx_6668'), (15, b'dx_70887'), (17, b'yy'), (18, b'yongfa'), (12, b'fenghuang'), (16, b'yongshi'), (27, b'ruiyin'), (26, b'java')]),
        ),
        migrations.AlterUniqueTogether(
            name='cdn_account_t',
            unique_together=set([('name', 'account')]),
        ),
    ]
