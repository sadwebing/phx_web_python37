# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dns', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cf_account',
            name='email',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='cf_account',
            name='key',
            field=models.CharField(default='a', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cf_account',
            name='name',
            field=models.CharField(default='a', unique=True, max_length=32),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='cf_account',
            unique_together=set([]),
        ),
    ]
