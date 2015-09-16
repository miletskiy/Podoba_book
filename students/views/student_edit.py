# -*- coding: utf-8 -*-

from django.shortcuts import render
from django import forms

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from ..models.student import Student
from ..models.group import Group

from studentsdb.settings import ADMIN_EMAIL

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit

from django.contrib import messages
# from contact_form.forms import ContactForm

# class KontaktForm(contact_form.forms.ContactForm):


class StudentEdit(forms.Form):

    # def __init__(self, *args, **kwargs):
    #     # call original initializator
    #     super(ContactForm, self).__init__(*args, **kwargs)

    #     # this helper object allows us to customize form
    #     self.helper = FormHelper()

    #     # form tag attributes
    #     self.helper.form_class = 'form-horizontal col-xs-10'
    #     self.helper.form_method = 'post'
    #     self.helper.form_action = reverse('contact_admin')

    #     # twitter bootstrap styles
    #     self.helper.help_text_inline = True
    #     self.helper.html5_required = True
    #     self.helper.label_class = 'col-sm-2 control-label'
    #     self.helper.field_class = 'col-sm-10'

    #     # form buttons
    #     self.helper.add_input(Submit('send_button', u'Надіслати'))
    groups = Group.objects.all().order_by('title')

    # student = Student.objects.all().filter_by(pk=request.POST['pk'])

    first_name = forms.CharField(
        label=u"Имя",
        max_length=128)
    last_name = forms.CharField(
        label=u"Фамилия",
        max_length=128)
    middle_name = forms.CharField(
        label=u"Отчество",
        max_length=128)
    birthday = forms.DateField(
        label=u"Дата рождения",
        input_formats='%Y-%m-%d')
    photo = forms.ImageField(
        label=u"Дата рождения")
    ticket = forms.CharField(
        label=u"Билет",
        max_length=8)

    notes = forms.CharField(
        label=u"Дополнительные заметки",
        max_length=2560,
        widget=forms.Textarea)

    student_group = forms.ModelChoiceField(groups)

    # from_email = forms.EmailField(
    #     label=u"Ваша емейл адреса")

    # subject = forms.CharField(
    #     label=u"Заголовок листа",
    #     max_length=128)

    # message = forms.CharField(
    #     label=u"Дополнительные заметки",
    #     max_length=2560,
    #     widget=forms.Textarea)


def student_edit(request,pk):
    # check if form was posted
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        student = StudentEdit(request.POST.pk)

        # check whether user data is valid:
        if student.is_valid(): # send email
            # student = Student(
            #                   first_name=request.POST['first_name'],
            #                   last_name=request.POST['last_name'],
            #                   middle_name=request.POST['middle_name'],
            #                   birthday=request.POST['birthday'],
            #                   ticket=request.POST['ticket'],
            #                   student_group=Group.objects.get(pk=request.POST['student_group']),
            #                   photo=request.FILES['photo'],
            #                  )
            student.save()
            #
            # subject = form.cleaned_data['subject']
            # message = form.cleaned_data['message']
            # from_email = form.cleaned_data['from_email']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # middle_name = form.cleaned_data['middle_name']
            # birthday = form.cleaned_data['birthday']
            # photo = form.cleaned_data['photo']
            # ticket = form.cleaned_data['ticket']
            # notes = form.cleaned_data['notes']
            # student_group = form.cleaned_data[
            # try:
            #     send_mail(subject, message, from_email, [ADMIN_EMAIL])
            # except Exception:
            #     message = u"Під час відправки листа виникла непередбачувана помилка. \
            #     Спробуйте скористатись даною формою пізніше. "
            # else:
            #     # message = u"Повідомлення успішно надіслане!"
            #     # message = u"Повідомлення успішно надіслане!"
            messages.success(request, u'messages Повідомлення успішно надіслане!! !')

            # redirect to same contact page with success message
            # return HttpResponseRedirect(
            #     u'%s?status_message=%s' % (reverse('student_edit'),message))
            return HttpResponseRedirect(reverse('student_edit'),messages)
            # return super(StudentEdit, self).post(request, *args, **kwargs)

    # if there was not POST render blank form
    else:
        student = StudentEdit(request.POST)

    return render(request, 'student_edit/forms.html', {'student': student})















