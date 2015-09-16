# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.shortcuts import render
from contact_form import forms
# from contact_form.forms import ContactForm

# import RequestSite from django.contrib.sites.requests.
#   site = RequestSite(self.request)
from django.contrib.sites.requests import RequestSite

class KontaktAdmin(forms.ContactForm):

    # def __init__(self, *args, **kwargs):
    #     super(KontaktAdmin, self).__init__(request=request,*args, **kwargs)
    # fields_keyOrder = ['reason', 'name', 'email', 'body']
    site = RequestSite(self.request)

# class CustomContactForm(ContactForm):
#     def __init__(self, request, *args, **kwargs):
#         super(CustomContactForm, self).__init__(request=request, *args, **kwargs)
#         fields_keyOrder = ['reason', 'name', 'email', 'body', 'captcha']
#         if (self.fields.has_key('keyOrder')):
#             self.fields.keyOrder = fields_keyOrder
#         else:
#             self.fields = OrderedDict((k, self.fields[k]) for k in fields_keyOrder)
#
#     REASON = (
#         ('support', 'Support'),
#         ('feedback', 'Feedback'),
#         ('delete', 'Account deletion')
#     )
#
#     template_name = 'contact_form/contact_form.txt'
#     subject_template_name = "contact_form/contact_form_subject.txt"
