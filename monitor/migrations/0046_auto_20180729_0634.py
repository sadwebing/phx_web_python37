# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0045_auto_20180729_0412'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='telegram_domain_alert_t',
            unique_together=set([('product', 'customer')]),
        ),
    ]
