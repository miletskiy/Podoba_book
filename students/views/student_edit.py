# -*- coding: utf-8 -*-

from django.shortcuts import render


from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from ..models.student import Student
from ..models.group import Group

from django import forms
from django.forms import ModelForm
from django.contrib import messages


class StudentEdit(ModelForm):

    class Meta:
        model = Student
        fields = []

    groups = Group.objects.all().order_by('title')

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


def student_edit(request, pk):
    # check if form was posted
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        student = StudentEdit(request.POST.pk)

        # check whether user data is valid:
        if student.is_valid():  # send email

            student.save()

            messages.success(
                request, u'messages Повідомлення успішно надіслане!! !')

            return HttpResponseRedirect(reverse('student_edit'), messages)

    # if there was not POST render blank form
    else:
        student = StudentEdit(request.POST)

    return render(request, 'student_edit/forms.html', {'student': student})
