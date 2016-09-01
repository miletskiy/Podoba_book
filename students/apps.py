# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
# Make handler for migrate
from django.db.models.signals import post_migrate


class StudentsAppConfig(AppConfig):
    name = 'students'
    verbose_name = _(u'Students Database')

    def ready(self):
        from students import signals
