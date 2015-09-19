# -*- coding: utf-8 -*-

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr

# from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

from ..models.student import  Student
from ..models.monthjournal import MonthJournal
from ..util import paginate#, get_current_group


class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self,**kwargs):
        # get context data from TemplateView class
        context = super(JournalView, self).get_context_data(**kwargs)

        # check if we need to display some specific month
        if self.request.GET.get('month'):
            month = datetime.strptime(self.request.GET['month'], '%Y-%m-%d'
                ).date()
        else:
            # otherwise just displaying current month data
            today = datetime.today()
            month = date(today.year, today.month, 1)
        # prev_month = month
        # next_month = month

        # calculate current, previous and next month details;
        # we need this for month navigation element in template
        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)
        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['year'] = month.year
        context['month_verbose'] = month.strftime('%B')

        # we'll use this variable in students pagination
        context['cur_month'] = month.strftime('%Y-%m-%d')

        # prepare variable for template to generate
        # journal table header elements
        myear, mmonth = month.year, month.month
        number_of_days = monthrange(myear, mmonth)[1]
        context['month_header'] = [{'day': d,
            'verbose': day_abbr[weekday(myear, mmonth, d)][:2]}
            for d in range(1, number_of_days+1)]

        # context['cur_month'] = '2015-09-01'
        # context['month_verbose'] = u"Вересень"


        # context['month_header'] = [
        #     {'day': 1, 'verbose': 'Пн'},
        #     {'day': 2, 'verbose': 'Вт'},
        #     {'day': 3, 'verbose': 'Cр'},
        #     {'day': 4, 'verbose': 'Чт'},
        #     {'day': 5, 'verbose': 'Пт'}]

        queryset = Student.objects.all().order_by('last_name')

        update_url = reverse('journal')

        # go over all students and collect data about presence
        # during selected month
        students = []
        for student in queryset:
            # try to get journal object by month selected
            # month and current student
            try:
                journal = MonthJournal.objects.get(student=student, date=month)
            except Exception:
                journal = None

            # fill in days presence list for current student
            days = []
            for day in range(1, number_of_days+1):
                days.append({
                    'day': day,
                    'present': journal and getattr(journal, 'present_day%d' %
                        day, False) or False,
                    'date': date(myear, mmonth, day).strftime(
                        '%Y-%m-%d'),
                })

            students.append({
                'fullname': u'%s %s' % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })

        # apply pagination, 10 students per page
        context = paginate(students, 5, self.request, context,
            var_name='students')

        # finally return updated context
        # with paginated students
        return context


# from django.shortcuts import render
# from django.http import HttpResponse

# # Views for Journal
# def journal_list(request):
#     # return HttpResponse('<h1>Journal urls</h1>')
#     students = (
#         {'id':1,
#         'first_name':u'Андрей',
#         'last_name':u'Корост',
#         'ticket':235,
#         },
#         {'id':2,
#         'first_name':u'Светлана',
#         'last_name':u'Ильдирова',
#         'ticket':2358,
#         },
#         {'id':3,
#         'first_name':u'Василий',
#         'last_name':u'Пупкин',
#         'ticket':2935,
#         },
#     )
#     return render(request, 'students/journal_list.html',
#         {'students': students})