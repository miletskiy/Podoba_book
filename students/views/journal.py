# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Views for Journal
def journal_list(request):
    # return HttpResponse('<h1>Journal urls</h1>')
    students = (
        {'id':1,
        'first_name':u'Андрей',
        'last_name':u'Корост',
        'ticket':235,
        },
        {'id':2,
        'first_name':u'Светлана',
        'last_name':u'Ильдирова',
        'ticket':2358,
        },
        {'id':3,
        'first_name':u'Василий',
        'last_name':u'Пупкин',
        'ticket':2935,
        },
    )
    return render(request, 'students/journal_list.html',
        {'students': students})