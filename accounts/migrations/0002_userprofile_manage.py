# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='manage',
            field=models.IntegerField(default=0, choices=[(1, b'\xe7\xae\xa1\xe7\x90\x86'), (0, b'\xe6\x99\xae\xe9\x80\x9a')]),
        ),
    ]
