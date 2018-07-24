# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0029_auto_20180724_1829'),
        ('accounts', '0004_delete_cdn_t'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='project',
            field=models.ManyToManyField(to='monitor.project_t', blank=True),
        ),
    ]
