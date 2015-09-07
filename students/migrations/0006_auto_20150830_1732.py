# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_student_student_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='starosta',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.Student', blank=True, verbose_name='\u0421\u0442\u0430\u0440\u043e\u0441\u0442\u0430'),
        ),
    ]
