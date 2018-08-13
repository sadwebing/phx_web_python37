# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0057_auto_20180813_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_t',
            name='project',
            field=models.CharField(max_length=10, choices=[('other', '\u5176\u4ed6[other]'), ('caipiao', '\u5f69\u7968[caipiao]'), ('sport', '\u4f53\u80b2[sport]'), ('houtai', '\u540e\u53f0[houtai]'), ('pay', '\u652f\u4ed8[pay]'), ('ggz', '\u5e7f\u544a\u7ad9[ggz]'), ('image', '\u56fe\u7247[image]'), ('vpn', 'vpn'), ('httpdns', 'httpdns')]),
        ),
        migrations.AlterField(
            model_name='telegram_domain_alert_t',
            name='project',
            field=models.CharField(blank=True, max_length=10, choices=[('other', '\u5176\u4ed6[other]'), ('caipiao', '\u5f69\u7968[caipiao]'), ('sport', '\u4f53\u80b2[sport]'), ('houtai', '\u540e\u53f0[houtai]'), ('pay', '\u652f\u4ed8[pay]'), ('ggz', '\u5e7f\u544a\u7ad9[ggz]'), ('image', '\u56fe\u7247[image]'), ('vpn', 'vpn'), ('httpdns', 'httpdns')]),
        ),
        migrations.AlterField(
            model_name='telegram_ssl_alert_t',
            name='project',
            field=models.CharField(blank=True, max_length=10, choices=[('other', '\u5176\u4ed6[other]'), ('caipiao', '\u5f69\u7968[caipiao]'), ('sport', '\u4f53\u80b2[sport]'), ('houtai', '\u540e\u53f0[houtai]'), ('pay', '\u652f\u4ed8[pay]'), ('ggz', '\u5e7f\u544a\u7ad9[ggz]'), ('image', '\u56fe\u7247[image]'), ('vpn', 'vpn'), ('httpdns', 'httpdns')]),
        ),
    ]
