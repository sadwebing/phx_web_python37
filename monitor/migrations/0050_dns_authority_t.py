# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dns', '0011_alter_history_action'),
        ('monitor', '0049_auto_20180805_1105'),
    ]

    operations = [
        migrations.CreateModel(
            name='dns_authority_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permission', models.CharField(max_length=10, choices=[('read', '\u8bfb\u6743\u9650'), ('change', '\u6539\u6743\u9650'), ('delete', '\u5220\u6743\u9650'), ('add', '\u589e\u6743\u9650')])),
                ('cf_account', models.ForeignKey(to='dns.cf_account', blank=True)),
                ('dnspod_account', models.ForeignKey(to='dns.dnspod_account', blank=True)),
            ],
        ),
    ]
