# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_userprofile_servers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='project',
        ),
    ]
