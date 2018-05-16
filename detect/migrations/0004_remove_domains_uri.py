# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0003_auto_20180516_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domains',
            name='uri',
        ),
    ]
