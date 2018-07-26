# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0037_auto_20180726_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_t',
            name='product',
            field=models.IntegerField(choices=[(0, '\u516c\u5171\u4ea7\u54c1[pub]'), (12, '\u51e4\u51f0[fenghuang]'), (16, '\u52c7\u58eb[yongshi]'), (27, '\u745e\u94f6[ruiyin|UBS]'), (26, 'JAVA')]),
        ),
    ]
