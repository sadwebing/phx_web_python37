# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='minion_ip_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minion_id', models.CharField(max_length=32)),
                ('ip_addr', models.GenericIPAddressField()),
                ('status', models.IntegerField(default=1, choices=[(1, '\u542f\u7528'), (0, '\u7981\u7528')])),
            ],
        ),
        migrations.CreateModel(
            name='project_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('envir', models.IntegerField(default=1, choices=[(1, '\u8fd0\u8425\u73af\u5883'), (0, '\u6d4b\u8bd5\u73af\u5883')])),
                ('product', models.IntegerField(choices=[(0, b'pub'), (1, b'ali'), (2, b'guangda'), (3, b'leying'), (4, b'caitou'), (5, b'tiantian'), (6, b'sande'), (7, b'uc'), (8, b'9393'), (9, b'3535'), (10, b'agcai'), (11, b'wanyou')])),
                ('project', models.CharField(max_length=64)),
                ('server_type', models.CharField(default='nginx', max_length=10, choices=[('nginx', 'nginx'), ('apache', 'apache')])),
                ('role', models.CharField(default='main', max_length=10, choices=[('main', 'main'), ('backup', 'backup')])),
                ('domain', models.CharField(max_length=128)),
                ('uri', models.CharField(default='/', max_length=128)),
                ('status', models.IntegerField(default=1, choices=[(1, '\u542f\u7528'), (0, '\u7981\u7528')])),
                ('info', models.CharField(max_length=128, null=True)),
                ('minion_id', models.ManyToManyField(to='monitor.minion_ip_t')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='minion_ip_t',
            unique_together=set([('minion_id', 'ip_addr')]),
        ),
    ]
