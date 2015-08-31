# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0011_auto_20150831_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='starosta',
            field=models.OneToOneField(blank=True, to='students.Student', null=True, verbose_name='Староста', on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
