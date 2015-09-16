# -*- coding: utf-8 -*-

from django.views.generic.edit import FormView
from ..views.contact_admin import ContactForm

from django.core.mail import send_mail
from django.contrib import messages

from studentsdb.settings import ADMIN_EMAIL

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render

class ContactAdmin(FormView):
    template_name = 'contact_admin/form.html'
    form_class = ContactForm
    success_url = '/'


    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        from_email = form.cleaned_data['from_email']
        send_mail(subject, message, from_email, [ADMIN_EMAIL])
        # messages.success(request, u'messages Повідомлення успішно надіслане!! !')
        return super(ContactAdmin, self).form_valid(form)

    def form_invalid(self, form):

        return super(ContactAdmin, self).form_invalid(form)