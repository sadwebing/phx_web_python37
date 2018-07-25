# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0030_project_authority_t'),
    ]

    operations = [
        migrations.AddField(
            model_name='minion_t',
            name='server_type',
            field=models.CharField(default='nginx', max_length=10, choices=[('nginx', 'nginx'), ('apache', 'apache'), ('vpn', 'vpn'), ('flask', 'flask')]),
        ),
    ]
