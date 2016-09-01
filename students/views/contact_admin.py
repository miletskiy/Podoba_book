
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
from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext as _


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
        self.helper.add_input(Submit('send_button', _(u'Send')))

    from_email = forms.EmailField(
        label=_(u'Your email'))

    subject = forms.CharField(
        label=_(u'Subject'),
        max_length=128)

    message = forms.CharField(
        label=_(u'Message for admin'),
        max_length=2560,
        widget=forms.Textarea)

# Signal after sending mail to admin 526
# Create signal.
email_was_send = Signal(providing_args=['subject', 'email'])

email_was_send.connect(simple_receiver)


def send_signal_email_for_admin(subject, email):
    email_was_send.send(sender='send_signal_email_for_admin',
                        subject=subject, email=email)


@permission_required('auth.add_user')
def contact_admin(request):
    # check if form was posted
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)

        # check whether user data is valid:
        if form.is_valid():  # send email
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']

            try:
                send_mail(subject, message, from_email, [ADMIN_EMAIL])
            except Exception:
                messages.error(request, _(u"When sending a letter, an unexpected error occurred.\
                 Try to use this form later."))
                logger = logging.getLogger(__name__)
                logger.exception('message')
            else:
                send_signal_email_for_admin(subject, from_email)
                mail_logger = logging.getLogger('email_was_send')
                mail_logger.info(
                    "Email from %s was send with next subject: %s", from_email, subject)
                messages.success(request, _(
                    u'The message was successfully sent'))

            # redirect to same contact page with success message
            return HttpResponseRedirect(reverse('contact_admin'))

    # if there was not POST render blank form
    else:
        form = ContactForm()

    return render(request, 'contact_admin/form.html', {'form': form})
