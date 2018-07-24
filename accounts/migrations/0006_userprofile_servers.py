# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0030_project_authority_t'),
        ('accounts', '0005_userprofile_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='servers',
            field=models.ManyToManyField(to='monitor.project_authority_t', blank=True),
        ),
    ]
