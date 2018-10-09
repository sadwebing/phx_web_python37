# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='domains',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(max_length=128)),
                ('uri', models.CharField(default=b'/', max_length=128)),
                ('product', models.CharField(max_length=32)),
                ('content', models.CharField(max_length=128)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='groups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.CharField(unique=True, max_length=128)),
                ('client', models.CharField(max_length=12)),
                ('method', models.CharField(max_length=12)),
            ],
        ),
        migrations.AddField(
            model_name='domains',
            name='group',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='name', to='detect.groups'),
        ),
    ]
