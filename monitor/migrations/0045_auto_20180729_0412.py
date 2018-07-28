# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0044_auto_20180729_0405'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegram_domain_alert_t',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, '\u542f\u7528'), (0, '\u7981\u7528')]),
        ),
        migrations.AddField(
            model_name='telegram_ssl_alert_t',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, '\u542f\u7528'), (0, '\u7981\u7528')]),
        ),
    ]
