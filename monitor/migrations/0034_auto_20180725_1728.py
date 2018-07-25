# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0033_auto_20180725_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_t',
            name='server_type',
            field=models.CharField(default='front', max_length=10, choices=[('front', '\u53cd\u4ee3\u670d\u52a1\u5668'), ('backend', '\u540e\u7aef\u6e90\u670d\u52a1\u5668'), ('other', '\u5176\u4ed6\u670d\u52a1\u5668')]),
        ),
        migrations.AlterUniqueTogether(
            name='project_t',
            unique_together=set([('product', 'project', 'envir', 'server_type')]),
        ),
    ]
