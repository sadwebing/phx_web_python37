# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('saltstack', '0003_auto_20170810_1743'),
    ]

    operations = [
        migrations.DeleteModel(
            name='tomcat_project',
        ),
        migrations.DeleteModel(
            name='tomcat_saltstack_history',
        ),
    ]
