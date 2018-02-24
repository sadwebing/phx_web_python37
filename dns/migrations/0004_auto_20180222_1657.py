# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dns', '0003_auto_20180222_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain_info',
            name='client',
            field=models.CharField(default='none', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='domain_info',
            name='product',
            field=models.CharField(default=True, max_length=32),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='domain_info',
            unique_together=set([('product', 'client', 'domain', 'route')]),
        ),
    ]
