# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class Student(models.Model):
    """Student Model"""

    first_name = models.CharField(
        max_length = 256,
        blank = False,
        verbose_name= u"Имя")

    last_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Фамилия")

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









