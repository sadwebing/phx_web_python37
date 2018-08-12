# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_user_project_authority_t_project'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='user_project_authority_t',
            unique_together=set([]),
        ),
    ]
