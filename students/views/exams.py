# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse ,HttpRequest
from django.template import RequestContext, loader

from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

from ..models.exam import Exam

# Views for Exams
def exams_list(request):

    exams = Exam.objects.all().order_by('nazva')

    # Order exams list
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'nazva','exam_day','prepod'):
        exams = exams.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            exams = exams.reverse()

    # Paginate exams
    paginator = Paginator(exams, 4)
    page = request.GET.get('page')
    try:
        exams = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        exams = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver
        # last page of results.
        exams = paginator.page(paginator.num_pages)


    return render(request, 'students/exams_list.html',
        {'exams': exams })
    
def exams_add(request):
    return HttpResponse('<h1>Exam Add Form</h1>')

def exams_edit(request,eid):
    return HttpResponse('<h1>Edit Exam %s</h1>' % eid)

def exams_delete(request,eid):
    return HttpResponse('<h1>Delete Exam %s</h1>' % eid)



    # exams = (
    #     {'id':1,
    #     'nazva':u'Основи Python',
    #     'datetime':u'2015-09-12 10:00',
    #     'prepod':u'Гвидо ван Россум',
    #     'group':u'КПИ 1й курс'
    #     },
    #     {'id':2,
    #     'nazva':u'Основи Django',
    #     'datetime':u'2015-09-16 10:42',
    #     'prepod':u'Адриан Головатый',
    #     'group':u'КНАУ 1й курс'},
    #     {'id':3,
    #     'nazva':u'Основи SQL',
    #     'datetime':u'2015-09-20 10:42',
    #     'prepod':u'Николай Иванович',
    #     'group':u'Институт информатики 1й курс'},
    # )
