# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0007_auto_20180521_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_t',
            name='project',
            field=models.CharField(max_length=10, choices=[('caipiao', 'caipiao'), ('sport', 'sport'), ('cp_ht', 'cp_ht'), ('vpn', 'vpn')]),
        ),
        migrations.AlterField(
            model_name='project_t',
            name='server_type',
            field=models.CharField(default='nginx', max_length=10, choices=[('nginx', 'nginx'), ('apache', 'apache'), ('vpn', 'vpn')]),
        ),
    ]
