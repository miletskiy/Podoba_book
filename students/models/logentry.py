# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class LogEntry(models.Model):
    """Model for logging in database"""

    class Meta(object):
        verbose_name = _(u"Log Entry")
        verbose_name_plural = _(u"Log Entries")

    id_process = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=_(u"Process ID"))

    level = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Log Level"))

    date_time = models.DateTimeField(
        blank=False,
        null=True,
        verbose_name=_(u"Datetime event"))

    module = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Module name"))

    message = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Message"))

    # excptn = models.TextField(
    #     blank=True,
    #     verbose_name=_(u"Exceptions"))

    def __unicode__(self):
        return u"%s %s" % (self.level, self.module)
