# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20180127_1444'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='minion_t',
            unique_together=set([('minion_id', 'ip_addr')]),
        ),
    ]
