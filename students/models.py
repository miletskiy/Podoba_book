# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class Student(models.Model):
    """Student Model"""

    class Meta(object):
        verbose_name=u"Студент"
        verbose_name_plural=u"Студенты"

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

    # number = models.CharField(
    #     max_length = 6,
    #     )

    def __unicode__(self):
        return u"%s %s" % (self.first_name,self.last_name)
    # def __unicode__(self):
    #     return u"%s %s" % (unicode(self.first_name),unicode(self.last_name))

    student_group = models.ForeignKey('Group',
        verbose_name=u"Група",
        blank=False,
        null=True,
        on_delete=models.PROTECT)

class Group(models.Model):
    """Group Model"""


    class Meta(object):
        verbose_name=u"Група"
        verbose_name_plural=u"Групи"

    title = models.CharField(
        max_length = 256,
        blank = False,
        verbose_name= u"Назва")


    starosta = models.OneToOneField('Student',
        verbose_name=u"Староста",
        blank=True,
        null = True,
        on_delete = models.SET_NULL,
        )


    notes = models.TextField(
        blank=True,
        verbose_name=u"Дополнительные заметки")

    def __unicode__(self):
        if self.starosta:
            return u"%s (%s %s)" % (self.title,self.starosta.first_name,self.starosta.last_name)
        else:
            return u"%s" % (self.title,)

    #     if self.starosta:
    #         return u"%s (%s %s)" % (unicode(self.title),unicode(self.starosta.first_name),unicode(self.starosta.last_name))
    #     else:
    #         return u"%s" % (unicode(self.title),)







