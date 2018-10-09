# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0013_auto_20180625_1635'),
        ('monitor', '0012_remove_project_t_domain'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_t',
            name='domain',
            field=models.ForeignKey(default=1, to='detect.domains', on_delete=models.CASCADE),
        ),
    ]
