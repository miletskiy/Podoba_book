# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse ,HttpRequest , HttpResponseRedirect
from django.template import RequestContext, loader

from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

from ..models.group import Group

from django.views.generic import DeleteView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.messages import get_messages

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


# Delete group with django generic views
class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'


    def get_success_url(self):
        return reverse('groups')
        # return reverse('home')

    def post(self, request, *args, **kwargs):
        group = self.get_object()
        messages.success(request, u'Групу %s успішно messages видалено!! messages!'% group )

        return super(GroupDeleteView,self).post(request,*args,**kwargs)


# Delete group WITHOUT django generic views
class GroupDelete(object):
    model = Group

    # group = Group.objects.all().filter(pk = request.POST.get())


# def groups_delete_my(request,pk):
#
#     # grup = self.get_object()
#     group = Group.objects.all().filter(pk = request.POST.get('pk'))
#     group.delete()
#     messages.success(request, u'Групу  успішно messages видалено!! !')#%s % grup)
#
#     return HttpResponseRedirect(reverse('home'),messages)
#     # return HttpResponse('<h1>Delete Group %s</h1>' % gid)

def groups_delete_my(request, pk):
    # group = Group.objects.all().filter(pk = request.POST.get('pk'))
    # grup = self.get_object()
    # title = Group.objects.all().filter(pk = pk).title
    group = Group.objects.get(pk = pk)
    title = group.title

    # group = Group.objects.all().filter(pk = pk)
    group.delete()
    messages.success(request, u'Групу %s успішно messages видалено!! !' % title)
    return HttpResponseRedirect(reverse('groups'),messages)
