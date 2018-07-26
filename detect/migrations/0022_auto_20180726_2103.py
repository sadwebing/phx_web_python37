# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0021_auto_20180726_2102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='domains',
            old_name='product',
            new_name='customer',
        ),
    ]
