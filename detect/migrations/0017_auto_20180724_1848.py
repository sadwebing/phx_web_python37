# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0016_auto_20180724_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domains',
            name='cdn',
            field=models.ManyToManyField(to='detect.cdn_account_t', blank=True),
        ),
    ]
