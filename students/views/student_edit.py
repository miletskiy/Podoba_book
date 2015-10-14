# -*- coding: utf-8 -*-

from django.shortcuts import render


from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from ..models.student import Student
from ..models.group import Group

from django.contrib import messages

from django import forms

from django.forms import ModelForm

# class StudentEdit(ModelForm):forms.Form
#     class Meta:
#         model = Student
#         fields = '__all__'

class StudentEdit(ModelForm):
    class Meta:
        model=Student
        fields = []

    groups = Group.objects.all().order_by('title')

    # student = Student.objects.all()

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

    student_group = forms.ModelChoiceField(
        groups,
        empty_label=u"Выберите группу",
        label=u"Група студента")



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




