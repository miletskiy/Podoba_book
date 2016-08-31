
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Group(models.Model):
    """Group Model"""

    class Meta(object):
        verbose_name = _(u"Group")
        verbose_name_plural = _(u"Groups")

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Title"))

    starosta = models.OneToOneField('Student',
                                    verbose_name=_(u"Leader"),
                                    blank=True,
                                    null=True,
                                    on_delete=models.SET_NULL,
                                    )

    notes = models.TextField(
        blank=True,
        verbose_name=_(u"Notes")
    )

    def __unicode__(self):
        if self.starosta:
            return u"%s ( %s %s)" % (self.title, self.starosta.first_name,
                                     self.starosta.last_name)
        else:
            return u"%s" % (self.title,)
