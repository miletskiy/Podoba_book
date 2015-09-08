# -*- coding: utf-8 -*-

from django.db import models


class Exam(models.Model):
    """Exam Model"""

    class Meta(object):
        verbose_name = u"Icпит"
        verbose_name_plural = u"Icпити"

    nazva = models.CharField(
        max_length = 256,
        blank = False,
        verbose_name= u"Назва предмету")

    exam_day = models.DateTimeField(
        blank=False,
        verbose_name=u"Дата проведення",
        null = True)

    prepod = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Викладач")
    

    exam_group = models.ForeignKey('Group',
        verbose_name=u"Група icпиту",
        blank=False,
        null=True,
        on_delete=models.PROTECT)


    notes = models.TextField(
        blank=True,
        verbose_name=u"Дополнительные заметки")


    def __unicode__(self):
        return u"%s (%s)" % (self.nazva,self.prepod)
