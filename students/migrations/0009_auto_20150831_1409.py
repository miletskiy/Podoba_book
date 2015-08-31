# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_auto_20150831_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='starosta',
            field=models.OneToOneField(blank=True, null=True, to='students.Student', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Староста'),
        ),
    ]
