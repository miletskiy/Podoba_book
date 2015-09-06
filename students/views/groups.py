# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse ,HttpRequest
from django.template import RequestContext, loader

from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

from ..models.group import Group

# Views for Groups
def groups_list(request):
    groups = Group.objects.all().order_by('title')

    # Order groups list
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'title', 'starosta'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    # Paginate groups
    paginator = Paginator(groups, 3)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        groups = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver
        # last page of results.
        groups = paginator.page(paginator.num_pages)

    # groups_kolvo = paginator.page(paginator.count) не получилось((


#     groups = (
#         {'id':1,
#         'nazva':u'Мтм-21',
#         'starosta':u'Ячменев Олег'},
#         {'id':2,
#         'nazva':u'Мтм-22',
#         'starosta':u'Виталий Подоба'},
#         {'id':3,
#         'nazva':u'Мтм-23',
#         'starosta':u'Иванов Андрей'},
#     )
    return render(request, 'students/groups_list.html',
        {'groups': groups })
    
def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')
    # pq = HttpRequest.path
    # zaq = str(pq)
    # # pq = RequestContext(request, {})
    # return HttpResponse(zaq)пока ничего не получилось.

def groups_edit(request,gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request,gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)
