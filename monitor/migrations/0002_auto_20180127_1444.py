# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='project_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('envir', models.CharField(default='ONLINE', max_length=10)),
                ('product', models.CharField(max_length=64)),
                ('project', models.CharField(max_length=64)),
                ('minion_id', models.CharField(max_length=32, null=True)),
                ('server_type', models.CharField(default='nginx', max_length=10)),
                ('role', models.CharField(default='main', max_length=16)),
                ('domain', models.CharField(max_length=128)),
                ('uri', models.CharField(max_length=128, null=True)),
                ('status', models.IntegerField(default=1)),
                ('info', models.CharField(max_length=128, null=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='tomcat_url',
            new_name='minion_t',
        ),
        migrations.AlterUniqueTogether(
            name='project_t',
            unique_together=set([('product', 'project', 'minion_id')]),
        ),
    ]
