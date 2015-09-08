# -*- coding: utf-8 -*-

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

from ..models.student import Student
from ..models.group import Group

from datetime import datetime

def students_list(request):
    students = Student.objects.all().order_by('last_name')

    # try to order students list
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket','id'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # paginate students
    paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver
        # last page of results.
        students = paginator.page(paginator.num_pages)


    return render(request,'students/students_list.html',
        {'students':students})

# Views for students
# def students_list(request):
#     students = (
#         {'id':1,
#         'first_name':u'Андрей',
#         'last_name':u'Корост',
#         'ticket':235,
#         'image': 'img/me.jpeg'},
#         {'id':2,
#         'first_name':u'Светлана',
#         'last_name':u'Ильдирова',
#         'ticket':2358,
#         'image': 'img/piv.png'},
#         {'id':3,
#         'first_name':u'Василий',
#         'last_name':u'Пупкин',
#         'ticket':2935,
#         'image': 'img/podoba3.jpg'},
#     )
#     return render(request, 'students/students_list.html',
#         {'students': students})


def students_add(request):
    # return HttpResponse('<h1>Student Add Form</h1>')
    # if form was post:
    if request.method == "POST":
        # if button add:
        if request.POST.get('add_button') is not None:
            # check data and collect mistakes
            # TODO: validate input from user
            errors = {}
            # validate student data will go here
            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}
            # validate user input
            first_name = request.POST.get('first_name', '').strip() 
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим" 
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip() 
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим" 
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip() 
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язково"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u'Введіть коректний формат дати (напр. 1984-12-31)'
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip() 
            if not ticket:
                errors['ticket'] = u"Номер білета є обов'язковим" 
            else:
                data['ticket'] = ticket
            
            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) !=1:
                    errors['student_group'] = u"Оберіть коректну групу для студента"
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo') 
            if photo:
                    data['photo'] = photo

            # if data correct:
            if not errors:
                # add student to base
                student = Student(**data)
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
                # return to students list
                return HttpResponseRedirect(
                    u'%s?status_message=Студента %s успішно додано!' %
                        (reverse('home'),Student.objects.last()))


            # if data incorrect:
            else:
                # return form with mistakes
                return render(request, 'students/students_add.html',
                                {'groups': Group.objects.all().order_by('title'),
                                 'errors': errors})
        # if button cancel:
        elif request.POST.get('cancel_button') is not None:
            # return to students list
            return HttpResponseRedirect(
                u'%s?status_message=Додавання студента скасовано!' %
                reverse('home'))
    # if form was NOT post:
    else:
        # return form 
        return render(request, 'students/students_add.html',
                        {'groups': Group.objects.all().order_by('title')})



    return render(request,'students/students_add.html',
        {'groups':Group.objects.all().order_by('title')})


def students_edit(request,sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request,sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
