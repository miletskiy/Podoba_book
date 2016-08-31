
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Exam(models.Model):
    """Exam Model"""

    class Meta(object):
        verbose_name = _(u"Exam")
        verbose_name_plural = _(u"Exams")

    nazva = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Exam Subject"))

    exam_day = models.DateTimeField(
        blank=False,
        verbose_name=_(u"Exam Date"),
        null=True)

    prepod = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Exam Teacher"))

    exam_group = models.ForeignKey('Group',
                                   verbose_name=_(u"Exam Group"),
                                   blank=False,
                                   null=True,
                                   on_delete=models.PROTECT)

    notes = models.TextField(
        blank=True,
        verbose_name=_(u"Notes"))

    def __unicode__(self):
        return u"%s (%s)" % (self.nazva, self.prepod)
