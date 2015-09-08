# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0013_exam'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exam',
            options={'verbose_name': 'Ic\u043f\u0438\u0442', 'verbose_name_plural': 'Ic\u043f\u0438\u0442\u0438'},
        ),
        migrations.AlterField(
            model_name='exam',
            name='exam_day',
            field=models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u043d\u044f'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='exam_group',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, verbose_name='\u0413\u0440\u0443\u043f\u0430 ic\u043f\u0438\u0442\u0443', to='students.Group'),
        ),
    ]
