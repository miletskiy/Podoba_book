# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render
from django import forms

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from studentsdb.settings import ADMIN_EMAIL

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.contrib import messages

from django.dispatch import Signal
# from students.signals import send_signal_email_for_admin
# from contact_form.forms import ContactForm

# class KontaktForm(contact_form.forms.ContactForm):



class ContactForm(forms.Form):

    def __init__(self, *args, **kwargs):
        # call original initializator
        super(ContactForm, self).__init__(*args, **kwargs)

        # this helper object allows us to customize form
        self.helper = FormHelper()

        # form tag attributes
        self.helper.form_class = 'form-horizontal col-xs-10'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_admin')

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # form buttons
        self.helper.add_input(Submit('send_button', u'Надіслати'))

    from_email = forms.EmailField(
        label=u"Ваша емейл адреса")

    subject = forms.CharField(
        label=u"Заголовок листа",
        max_length=128)

    message = forms.CharField(
        label=u"Текст повідомлення",
        max_length=2560,
        widget=forms.Textarea)

# Signal after sending mail to admin 526
# Create signal.
email_was_send = Signal(providing_args=['subject','email'])

# These function is receiver. It will receive
# the signal sent  by the sender.
def simple_receiver(**kwargs):
    # subject, email = kwargs['subject'], kwargs['email']
    # print 'Receiver # 1'
    # print '\tsubject: %s, email: %s\n' % (subject, email)
    pass

email_was_send.connect(simple_receiver)

def send_signal_email_for_admin(subject,email):
    email_was_send.send(sender='send_signal_email_for_admin', subject=subject, email=email)



def contact_admin(request):
    # check if form was posted
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)

        # check whether user data is valid:
        if form.is_valid(): # send email
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']

            try:
                send_mail(subject, message, from_email, [ADMIN_EMAIL])
            except Exception:
                # message = u"Під час відправки листа виникла непередбачувана помилка. \
                # Спробуйте скористатись даною формою пізніше. "
                messages.error(request,u"Під час відправки листа виникла непередбачувана помилка. \
                 Спробуйте скористатись даною формою пізніше. " )
                logger = logging.getLogger(__name__)
                logger.exception('message')
            else:
                send_signal_email_for_admin(subject,from_email)
                # mail_logger=logging.getLogger(__name__)
                mail_logger=logging.getLogger('email_was_send')
                # mail_logger.log('error','custom message',from_email, subject)
                # mail_logger.error("Email from %s was send with next subject: %s", from_email, subject)
                mail_logger.info("Email from %s was send with next subject: %s", from_email, subject)
                # message = u"Повідомлення успішно надіслане!"
                messages.success(request, u'messages Повідомлення успішно надіслане!! !')

            # redirect to same contact page with success message
            # return HttpResponseRedirect(
            #     u'%s?status_message=%s' % (reverse('contact_admin'),message))
            return HttpResponseRedirect(reverse('contact_admin'))

    # if there was not POST render blank form
    else:
        form = ContactForm()


    return render(request, 'contact_admin/form.html', {'form': form})















