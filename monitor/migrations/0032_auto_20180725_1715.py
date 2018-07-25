# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0031_minion_t_server_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='minion_t',
            old_name='server_type',
            new_name='service_type',
        ),
    ]
