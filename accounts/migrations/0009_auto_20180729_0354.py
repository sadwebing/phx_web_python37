# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20180729_0240'),
    ]

    operations = [
        migrations.DeleteModel(
            name='telegram_chat_group_t',
        ),
        migrations.DeleteModel(
            name='telegram_user_id_t',
        ),
    ]
