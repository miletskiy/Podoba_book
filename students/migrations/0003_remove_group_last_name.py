# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20150816_2050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='last_name',
        ),
    ]
