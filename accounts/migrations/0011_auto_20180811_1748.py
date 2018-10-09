# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0052_auto_20180811_1748'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0010_userprofile_dns'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_project_authority_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permission', models.ManyToManyField(to='monitor.permission_t')),
                ('project', models.ForeignKey(to='monitor.project_t', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='user_project_authority_t',
            unique_together=set([('user', 'project')]),
        ),
    ]
