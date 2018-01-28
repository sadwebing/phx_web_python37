# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('saltstack', '0002_salt_tomcat_history'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='salt_tomcat_history',
            new_name='tomcat_saltstack_history',
        ),
    ]
