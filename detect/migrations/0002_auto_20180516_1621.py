# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domains',
            name='group',
            field=models.ForeignKey(on_delete=models.CASCADE, to='detect.groups'),
        ),
    ]
