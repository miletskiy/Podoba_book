# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=256, verbose_name='\u0418\u043c\u044f')),
                ('last_name', models.CharField(max_length=256, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f')),
                ('middle_name', models.CharField(default=b'', max_length=256, verbose_name='\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e', blank=True)),
                ('birthday', models.DateField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f')),
                ('photo', models.ImageField(upload_to=b'', null=True, verbose_name='\u0424\u043e\u0442\u043e', blank=True)),
                ('ticket', models.CharField(max_length=256, verbose_name='\u0411\u0438\u043b\u0435\u0442')),
                ('notes', models.TextField(verbose_name='\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u0437\u0430\u043c\u0435\u0442\u043a\u0438', blank=True)),
            ],
        ),
    ]
