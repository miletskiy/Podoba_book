# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.models import LogEntry


def log_list(request):

    logs = LogEntry.objects.all()

    return render(request, 'students/log_list.html',
                  {'logs': logs})
