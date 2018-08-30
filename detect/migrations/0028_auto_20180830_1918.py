# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0027_auto_20180805_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domains',
            name='customer',
            field=models.IntegerField(choices=[(29, '\u516c\u5171\u5ba2\u6237[pub]'), (1, '\u963f\u91cc[ali]'), (2, '\u5149\u5927[guangda]'), (34, '\u6052\u8fbe[hengda]'), (3, '\u4e50\u76c8|\u718a\u732b[leying]'), (4, '\u5f69\u6295[caitou]'), (5, '\u5929\u5929[tiantian]'), (6, '\u4e09\u5fb7|\u5bcc\u8c6a|668[sande]'), (7, 'uc\u5f69\u7968[uc]'), (8, '\u8c37\u6b4c[9393]'), (9, '\u82f9\u679c[3535]'), (19, '\u8292\u679c[1717]'), (10, 'ag\u5f69[agcai]'), (23, '\u4ebf\u817e[yiteng]'), (24, '\u6c38\u5229\u4f1a[yonglihui]'), (25, '618\u5f69[618cai]'), (28, '\u4e50\u5929[letian]'), (21, '\u4e50\u90fd\u57ce[leducheng]'), (11, '\u4e07\u6e38[wanyou]'), (17, 'yy\u5a31\u4e50\u57ce[yy]'), (18, '\u6c38\u53d1[yongfa]'), (13, '\u94bb\u77f3[le7]'), (14, '\u5927\u8c616668[dx_6668]'), (15, '\u5927\u8c6170887[dx_70887]'), (30, '\u5927\u8c61[daxiang]'), (32, '\u4e16\u5fb7[shide]'), (33, '\u56fe\u817e[tuteng]'), (31, '\u6052\u9686[henglong]')]),
        ),
    ]
