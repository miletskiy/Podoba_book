
# -*- coding: utf-8 -*-
# view
from contact_form.views import ContactFormView
from django.core.urlresolvers import reverse


from ..views.form import KontaktForm

from django.contrib.sites.requests import RequestSite


class KontaktView(ContactFormView):
    form_class = KontaktForm



    def get_success_url(self):
        # site = RequestSite(self.request)
        # This is in a method instead of the success_url attribute
        # because doing it as an attribute would involve a
        # module-level call to reverse(), creating a circular
        # dependency between the URLConf (which imports this module)
        # and this module (which would need to access the URLConf to
        # make the reverse() call).
        return reverse('home')



