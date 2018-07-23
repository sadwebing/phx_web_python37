# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0027_auto_20180722_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_t',
            name='svn',
            field=models.IntegerField(default=1, choices=[(1, '\u542f\u7528'), (0, '\u7981\u7528')]),
        ),
        migrations.AlterField(
            model_name='project_t',
            name='project',
            field=models.CharField(max_length=10, choices=[('caipiao', 'caipiao'), ('sport', 'sport'), ('houtai', 'houtai'), ('ggz', 'ggz'), ('vpn', 'vpn'), ('image', 'image'), ('httpdns', 'httpdns')]),
        ),
        migrations.AlterField(
            model_name='project_t',
            name='server_type',
            field=models.CharField(default='nginx', max_length=10, choices=[('nginx', 'nginx'), ('apache', 'apache'), ('vpn', 'vpn'), ('flask', 'flask')]),
        ),
    ]
