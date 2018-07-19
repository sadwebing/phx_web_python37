# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dns', '0009_dnspod_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='alter_history',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
