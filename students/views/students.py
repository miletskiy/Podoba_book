# -*- coding: utf-8 -*-

from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse

# Views for students
def students_list(request):
    students = (
        {'id':1,
        'first_name':u'Андрей',
        'last_name':u'Корост',
        'ticket':235,
        'image': 'img/me.jpeg'},
        {'id':2,
        'first_name':u'Светлана',
        'last_name':u'Ильдирова',
        'ticket':2358,
        'image': 'img/piv.png'},
        {'id':3,
        'first_name':u'Василий',
        'last_name':u'Пупкин',
        'ticket':2935,
        'image': 'img/podoba3.jpg'},
    )
    return render(request, 'students/students_list.html',
        {'students': students})


def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>') 

def students_edit(request,sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request,sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
