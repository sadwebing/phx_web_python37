# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0004_remove_domains_uri'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='ssl',
            field=models.IntegerField(default=1),
        ),
    ]
