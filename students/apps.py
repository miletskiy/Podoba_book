# -*- coding: utf-8 -*-
from django.apps import AppConfig
# Make handler for migrate
from django.db.models.signals import post_migrate

# Receiver for migrate
# def my_callback():
#     pass


class StudentsAppConfig(AppConfig):
    name = 'students'
    verbose_name = u'База студентив'

    def ready(self):
        from students import signals
        # post_migrate.connect(my_callback, sender=self)