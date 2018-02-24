# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dns', '0005_domain_info_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain_info',
            name='route_status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='domain_info',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
