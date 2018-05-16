# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0005_groups_ssl'),
    ]

    operations = [
        migrations.RenameField(
            model_name='domains',
            old_name='domain',
            new_name='name',
        ),
    ]
