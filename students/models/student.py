# -*- coding: utf-8 -*-

from django.db import models

class Student(models.Model):
    """Student Model"""

    class Meta(object):
        verbose_name=u"Студент"
        verbose_name_plural=u"Студенти"

    first_name = models.CharField(
        max_length = 256,
        blank = False,
        verbose_name= u"Имя")

    last_name = models.CharField(
        # help_text="Please use the following format: <em>YYYY-MM-DD</em>.",
        max_length=256,
        blank=False,
        verbose_name=u"Фамилия"
        )

    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"Отчество",
        default = '')

    birthday = models.DateField(
        blank=False,
        verbose_name=u"Дата рождения",
        null = True)

    photo = models.ImageField(
        blank=True,
        verbose_name=u"Фото",
        null=True)

    ticket = models.CharField(
        max_length=256,
        blank=False,
        verbose_name = u"Билет")

    notes = models.TextField(
        blank=True,
        verbose_name=u"Дополнительные заметки")

    student_group = models.ForeignKey('Group',
        verbose_name=u"Група",
        blank=False,
        null=True,
        on_delete=models.PROTECT)


    def __unicode__(self):
        return u"%s %s" % (self.first_name,self.last_name)


