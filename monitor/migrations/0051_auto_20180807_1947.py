# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0050_dns_authority_t'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dns_authority_t',
            name='cf_account',
            field=models.ForeignKey(blank=True, to='dns.cf_account', null=True),
        ),
        migrations.AlterField(
            model_name='dns_authority_t',
            name='dnspod_account',
            field=models.ForeignKey(blank=True, to='dns.dnspod_account', null=True),
        ),
    ]
