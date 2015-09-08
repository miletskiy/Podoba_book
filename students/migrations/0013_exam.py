# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0012_auto_20150831_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nazva', models.CharField(max_length=256, verbose_name='\u041d\u0430\u0437\u0432\u0430 \u043f\u0440\u0435\u0434\u043c\u0435\u0442\u0443')),
                ('exam_day', models.DateField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0438\u044f')),
                ('prepod', models.CharField(max_length=256, verbose_name='\u0412\u0438\u043a\u043b\u0430\u0434\u0430\u0447')),
                ('notes', models.TextField(verbose_name='\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u0437\u0430\u043c\u0435\u0442\u043a\u0438', blank=True)),
                ('exam_group', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, verbose_name='\u0413\u0440\u0443\u043f\u0430 \u044d\u043a\u0437\u0430\u043c\u0435\u043d\u0430', to='students.Group')),
            ],
            options={
                'verbose_name': '\u042d\u043a\u0437\u0430\u043c\u0435\u043d',
                'verbose_name_plural': '\u042d\u043a\u0437\u0430\u043c\u0435\u043d\u044b',
            },
        ),
    ]
