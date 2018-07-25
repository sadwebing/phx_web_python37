# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0034_auto_20180725_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_t',
            name='customer',
            field=models.CharField(default=29, max_length=10, choices=[(29, b'pub[\xe5\x85\xac\xe5\x85\xb1\xe5\xae\xa2\xe6\x88\xb7]'), (1, b'ali[\xe9\x98\xbf\xe9\x87\x8c]'), (2, b'guangda[\xe5\x85\x89\xe5\xa4\xa7]'), (3, b'leying[\xe4\xb9\x90\xe7\x9b\x88|\xe7\x86\x8a\xe7\x8c\xab]'), (4, b'caitou[\xe5\xbd\xa9\xe6\x8a\x95]'), (5, b'tiantian[\xe5\xa4\xa9\xe5\xa4\xa9]'), (6, b'sande[\xe4\xb8\x89\xe5\xbe\xb7|\xe5\xaf\x8c\xe8\xb1\xaa|668]'), (7, b'uc\xe5\xbd\xa9\xe7\xa5\xa8'), (8, b'9393[\xe8\xb0\xb7\xe6\xad\x8c]'), (9, b'3535[\xe8\x8b\xb9\xe6\x9e\x9c]'), (19, b'1717[\xe8\x8a\x92\xe6\x9e\x9c]'), (10, b'agcai[ag\xe5\xbd\xa9]'), (20, b'fulicai[\xe7\xa6\x8f\xe5\x88\xa9\xe5\xbd\xa9]'), (22, b'yrcai[\xe4\xba\xbf\xe4\xba\xba]'), (23, b'yiteng[\xe4\xba\xbf\xe8\x85\xbe]'), (24, b'yonglihui[\xe6\xb0\xb8\xe5\x88\xa9\xe4\xbc\x9a]'), (25, b'618cai[618\xe5\xbd\xa9]'), (28, b'letian[\xe4\xb9\x90\xe5\xa4\xa9]'), (21, b'leducheng[\xe4\xb9\x90\xe9\x83\xbd\xe5\x9f\x8e]'), (11, b'wanyou[\xe4\xb8\x87\xe6\xb8\xb8]'), (17, b'yy\xe5\xa8\xb1\xe4\xb9\x90\xe5\x9f\x8e'), (18, b'yongfa[\xe6\xb0\xb8\xe5\x8f\x91]'), (13, b'le7[\xe9\x92\xbb\xe7\x9f\xb3]'), (14, b'dx_6668[\xe5\xa4\xa7\xe8\xb1\xa16668]'), (15, b'dx_70887[\xe5\xa4\xa7\xe8\xb1\xa170887]')]),
        ),
        migrations.AlterField(
            model_name='minion_t',
            name='provider',
            field=models.IntegerField(default=1, choices=[(1, '\u53f0\u6e7e\u673a\u623f[taiwan]'), (2, '\u9999\u6e2f\u673a\u623f[hongkong]'), (3, 'fent'), (4, '\u661f\u8054[xinglian]'), (5, '\u4e45\u901f[jiusu]'), (6, '\u675c\u675c[dudu]'), (7, '\u7f51\u65f6[wangshi]'), (8, '\u4f18\u4e0e\u4e91[youyucloud]'), (9, '\u963f\u91cc\u4e91[alicloud]')]),
        ),
        migrations.AlterField(
            model_name='project_t',
            name='envir',
            field=models.IntegerField(default=1, choices=[(1, '\u8fd0\u8425\u73af\u5883[ONLINE]'), (0, '\u6d4b\u8bd5\u73af\u5883[TEST]')]),
        ),
        migrations.AlterField(
            model_name='project_t',
            name='product',
            field=models.IntegerField(choices=[(0, b'pub[\xe5\x85\xac\xe5\x85\xb1\xe4\xba\xa7\xe5\x93\x81]'), (1, b'ali[\xe9\x98\xbf\xe9\x87\x8c]'), (2, b'guangda[\xe5\x85\x89\xe5\xa4\xa7]'), (3, b'leying[\xe4\xb9\x90\xe7\x9b\x88|\xe7\x86\x8a\xe7\x8c\xab]'), (4, b'caitou[\xe5\xbd\xa9\xe6\x8a\x95]'), (5, b'tiantian[\xe5\xa4\xa9\xe5\xa4\xa9]'), (6, b'sande[\xe4\xb8\x89\xe5\xbe\xb7|\xe5\xaf\x8c\xe8\xb1\xaa|668]'), (7, b'uc'), (8, b'9393[\xe8\xb0\xb7\xe6\xad\x8c]'), (9, b'3535[\xe8\x8b\xb9\xe6\x9e\x9c]'), (19, b'1717[\xe8\x8a\x92\xe6\x9e\x9c]'), (10, b'agcai[ag\xe5\xbd\xa9]'), (20, b'fulicai[\xe7\xa6\x8f\xe5\x88\xa9\xe5\xbd\xa9]'), (22, b'yrcai[\xe4\xba\xbf\xe4\xba\xba]'), (23, b'yiteng[\xe4\xba\xbf\xe8\x85\xbe]'), (24, b'yonglihui[\xe6\xb0\xb8\xe5\x88\xa9\xe4\xbc\x9a]'), (25, b'618cai[618\xe5\xbd\xa9]'), (28, b'letian[\xe4\xb9\x90\xe5\xa4\xa9]'), (21, b'leducheng[\xe4\xb9\x90\xe9\x83\xbd\xe5\x9f\x8e]'), (11, b'wanyou[\xe4\xb8\x87\xe6\xb8\xb8]'), (13, b'le7[\xe9\x92\xbb\xe7\x9f\xb3]'), (14, b'dx_6668[\xe5\xa4\xa7\xe8\xb1\xa16668]'), (15, b'dx_70887[\xe5\xa4\xa7\xe8\xb1\xa170887]'), (17, b'yy'), (18, b'yongfa[\xe6\xb0\xb8\xe5\x8f\x91]'), (12, b'fenghuang[\xe5\x87\xa4\xe5\x87\xb0]'), (16, b'yongshi[\xe5\x8b\x87\xe5\xa3\xab]'), (27, b'ruiyin[\xe7\x91\x9e\xe9\x93\xb6|UBS]'), (26, b'java')]),
        ),
        migrations.AlterField(
            model_name='project_t',
            name='project',
            field=models.CharField(max_length=10, choices=[('caipiao', '\u5f69\u7968[caipiao]'), ('sport', '\u4f53\u80b2[sport]'), ('houtai', '\u540e\u53f0[houtai]'), ('pay', '\u652f\u4ed8[pay]'), ('ggz', '\u5e7f\u544a\u7ad9[ggz]'), ('image', '\u56fe\u7247[image]'), ('vpn', 'vpn'), ('httpdns', 'httpdns')]),
        ),
        migrations.AlterField(
            model_name='project_t',
            name='role',
            field=models.CharField(default='main', max_length=10, choices=[('main', '\u4e3b[main]'), ('backup', '\u5907[backup]')]),
        ),
        migrations.AlterField(
            model_name='project_t',
            name='server_type',
            field=models.CharField(default='front', max_length=10, choices=[('front', '\u53cd\u4ee3\u670d\u52a1\u5668[front]'), ('backend', '\u540e\u7aef\u6e90\u670d\u52a1\u5668[backend]'), ('other', '\u5176\u4ed6\u670d\u52a1\u5668[other]')]),
        ),
        migrations.AlterField(
            model_name='project_t',
            name='svn',
            field=models.IntegerField(default=0, choices=[(1, '\u542f\u7528'), (0, '\u7981\u7528')]),
        ),
    ]
