# -*- coding: utf-8 -*-

from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

from ..models.student import Student

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
    return HttpResponse('<h1>Student Add Form</h1>') 

def students_edit(request,sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request,sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
