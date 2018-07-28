# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0025_auto_20180729_0313'),
        ('monitor', '0041_auto_20180729_0301'),
    ]

    operations = [
        migrations.CreateModel(
            name='telegram_domain_alert_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('product', models.IntegerField(choices=[(0, '\u516c\u5171\u4ea7\u54c1[pub]'), (12, '\u51e4\u51f0[fenghuang]'), (16, '\u52c7\u58eb[yongshi]'), (27, '\u745e\u94f6[ruiyin|UBS]'), (26, 'JAVA')])),
                ('project', models.CharField(max_length=10, choices=[('caipiao', '\u5f69\u7968[caipiao]'), ('sport', '\u4f53\u80b2[sport]'), ('houtai', '\u540e\u53f0[houtai]'), ('pay', '\u652f\u4ed8[pay]'), ('ggz', '\u5e7f\u544a\u7ad9[ggz]'), ('image', '\u56fe\u7247[image]'), ('vpn', 'vpn'), ('httpdns', 'httpdns')])),
                ('chat_group', models.ManyToManyField(to='detect.telegram_chat_group_t')),
                ('user_id', models.ManyToManyField(to='detect.telegram_user_id_t', blank=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='telegram_domain_alert_t',
            unique_together=set([('product', 'project')]),
        ),
    ]
