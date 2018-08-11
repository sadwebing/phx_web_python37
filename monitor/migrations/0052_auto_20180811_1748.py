# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0051_auto_20180807_1947'),
    ]

    operations = [
        migrations.CreateModel(
            name='permission_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permission', models.CharField(unique=True, max_length=10, choices=[(b'read', b'\xe8\xaf\xbb\xe6\x9d\x83\xe9\x99\x90'), (b'change', b'\xe6\x94\xb9\xe6\x9d\x83\xe9\x99\x90'), (b'delete', b'\xe5\x88\xa0\xe6\x9d\x83\xe9\x99\x90'), (b'add', b'\xe5\xa2\x9e\xe6\x9d\x83\xe9\x99\x90'), (b'execute', b'\xe6\x89\xa7\xe8\xa1\x8c\xe6\x9d\x83\xe9\x99\x90')])),
            ],
        ),
        migrations.AlterField(
            model_name='dns_authority_t',
            name='permission',
            field=models.CharField(max_length=10, choices=[(b'read', b'\xe8\xaf\xbb\xe6\x9d\x83\xe9\x99\x90'), (b'change', b'\xe6\x94\xb9\xe6\x9d\x83\xe9\x99\x90'), (b'delete', b'\xe5\x88\xa0\xe6\x9d\x83\xe9\x99\x90'), (b'add', b'\xe5\xa2\x9e\xe6\x9d\x83\xe9\x99\x90'), (b'execute', b'\xe6\x89\xa7\xe8\xa1\x8c\xe6\x9d\x83\xe9\x99\x90')]),
        ),
    ]
