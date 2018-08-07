# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0051_auto_20180807_1947'),
        ('accounts', '0009_auto_20180729_0354'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='dns',
            field=models.ManyToManyField(to='monitor.dns_authority_t', blank=True),
        ),
    ]
