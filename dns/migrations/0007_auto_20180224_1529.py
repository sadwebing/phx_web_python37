# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dns', '0006_auto_20180224_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain_info',
            name='content',
            field=models.CharField(max_length=128),
        ),
    ]
