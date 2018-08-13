# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0056_auto_20180812_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minion_t',
            name='service_type',
            field=models.CharField(default='nginx', max_length=10, choices=[('nginx', 'nginx'), ('apache', 'apache'), ('vpn', 'vpn'), ('flask', 'flask'), ('logstash', 'logstash')]),
        ),
        migrations.AlterField(
            model_name='project_t',
            name='project',
            field=models.CharField(max_length=10, choices=[('pub', '\u516c\u5171\u9879\u76ee[pub]'), ('caipiao', '\u5f69\u7968[caipiao]'), ('sport', '\u4f53\u80b2[sport]'), ('houtai', '\u540e\u53f0[houtai]'), ('pay', '\u652f\u4ed8[pay]'), ('ggz', '\u5e7f\u544a\u7ad9[ggz]'), ('image', '\u56fe\u7247[image]'), ('vpn', 'vpn'), ('httpdns', 'httpdns')]),
        ),
        migrations.AlterField(
            model_name='telegram_domain_alert_t',
            name='project',
            field=models.CharField(blank=True, max_length=10, choices=[('pub', '\u516c\u5171\u9879\u76ee[pub]'), ('caipiao', '\u5f69\u7968[caipiao]'), ('sport', '\u4f53\u80b2[sport]'), ('houtai', '\u540e\u53f0[houtai]'), ('pay', '\u652f\u4ed8[pay]'), ('ggz', '\u5e7f\u544a\u7ad9[ggz]'), ('image', '\u56fe\u7247[image]'), ('vpn', 'vpn'), ('httpdns', 'httpdns')]),
        ),
        migrations.AlterField(
            model_name='telegram_ssl_alert_t',
            name='project',
            field=models.CharField(blank=True, max_length=10, choices=[('pub', '\u516c\u5171\u9879\u76ee[pub]'), ('caipiao', '\u5f69\u7968[caipiao]'), ('sport', '\u4f53\u80b2[sport]'), ('houtai', '\u540e\u53f0[houtai]'), ('pay', '\u652f\u4ed8[pay]'), ('ggz', '\u5e7f\u544a\u7ad9[ggz]'), ('image', '\u56fe\u7247[image]'), ('vpn', 'vpn'), ('httpdns', 'httpdns')]),
        ),
    ]
