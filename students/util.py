# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import urllib


def paginate(objects, size, request, context, var_name='object_list'):
    """Paginate objects provided by view.
    This function takes:
      * list of elements;
      * number of objects per page;
      * request object to get url parameters from;
      * context to set new variables into;
      * var_name - variable name for list of objects.
    It returns updated context object."""
    # apply pagination
    paginator = Paginator(objects, size)
    # try to get page number from request
    page = request.GET.get('page', '1')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        object_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        object_list = paginator.page(paginator.num_pages)
    # set variables into context
    context[var_name] = object_list
    context['is_paginated'] = object_list.has_other_pages()
    context['page_obj'] = object_list
    context['paginator'] = paginator

    return context

# from .models.group import Group
def get_groups(request):
    """Returns list of existing groups"""
    # deferred import of Group model to avoid cycled imports
    from .models.group import Group

    # get currently selected group
    cur_group = get_current_group(request)


    groups = []
    # groups = Group.objects.all().order_by('title')
    for group in Group.objects.all().order_by('title'):
        groups.append({
            'id': group.id,
            'title': group.title,
            'starosta': group.starosta and (u'староста %s %s' % (group.starosta.first_name,
                group.starosta.last_name)) or None,
            'selected': cur_group and cur_group.id == group.id and True or False
        })
    return groups
    # return Group.objects.all().order_by('title')


def get_current_group(request):
    """Returns currently selected group or None"""

    # we remember selected group in a cookie
    kp = request.COOKIES.get('current_group')

    # pk = 2
    if kp:
        pk=urllib.unquote(kp).strip()
        from .models.group import Group
        try:
            # group = Group.objects.get(pk=int(qw))
            group = Group.objects.get(pk=int(pk))
        except Group.DoesNotExist:
            return None
        else:
            return group
    else:
        return None
#
# def get_language_cookie(request):
#
#     lng = request.COOKIES.get('current_lang')
#
#     if lng == 1:
#         request['LANGUAGE_CODE'] = 'uk'
#         return request['LANGUAGE_CODE']
#
#
#     elif lng == 2:
#         request['LANGUAGE_CODE']= 'en'
#         return request['LANGUAGE_CODE']
#
#     elif lng == 3:
#         request['LANGUAGE_CODE'] = 'pl'
#         return request['LANGUAGE_CODE']
#
#
# def get_current_language(request):
#
#     lang = request.COOKIES.get('current_lang')
#
#     languages = [
#                 {
#                 'value':1,
#                 'name':'Українська',
#                 'selected': False
#             },
#                 {
#                 'value':2,
#                 'name':'English',
#                 'selected': False
#             },
#                 {
#                 'value':3,
#                 'name':'Polski',
#                 'selected': False
#             },
#           ]
#
#     if lang:
#         i = int(lang) - 1
#         languages[i]['selected'] = True
#         # request.LANGUAGE_CODE = 'en'
#
#         return languages
#     else:
#         return languages
#
# from django.middleware.locale import LocaleMiddleware
#
# from django.utils import translation
#
# class LocalChooseLang(LocaleMiddleware):
#
#
#     def process_request(self, request):
#         check_path = self.is_language_prefix_patterns_used()
#         language = translation.get_language_from_request(
#             request, check_path=check_path)
#         translation.activate(language)
#
#         languages = get_current_language(request)
#
#         if languages[0]['selected']:
#             request.LANGUAGE_CODE = 'uk'
#
#         elif languages[1]['selected']:
#             request.LANGUAGE_CODE = 'en'
#
#         elif languages[2]['selected']:
#             request.LANGUAGE_CODE = 'pl'
#         else:
#             request.LANGUAGE_CODE = translation.get_language()
#


            



