# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0046_auto_20180729_0634'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='telegram_ssl_alert_t',
            unique_together=set([('product', 'customer')]),
        ),
    ]
