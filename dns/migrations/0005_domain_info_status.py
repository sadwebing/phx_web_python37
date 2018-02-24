# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dns', '0004_auto_20180222_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain_info',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
