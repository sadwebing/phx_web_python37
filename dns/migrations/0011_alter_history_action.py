# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dns', '0010_alter_history_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='alter_history',
            name='action',
            field=models.CharField(default='change', max_length=10, choices=[('change', '\u4fee\u6539'), ('add', '\u65b0\u589e'), ('delete', '\u5220\u9664')]),
        ),
    ]
