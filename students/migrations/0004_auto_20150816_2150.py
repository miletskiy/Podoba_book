# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_remove_group_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='starosta',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, default='\u0422\u0443\u0442 \u0441\u0430\u043c\u043e\u0443\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 :-)', to='students.Student', blank=True, verbose_name='\u0421\u0442\u0430\u0440\u043e\u0441\u0442\u0430'),
        ),
    ]
