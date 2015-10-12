# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.models import LogEntry

def log_list(request):
    # return HttpResponse('<h1>Events will come...</h1>')
    logs=LogEntry.objects.all()
    # LogEntry.

    return render(request,'students/log_list.html',
        {'logs':logs})


    # return render(request,'students/log_list.html',
    #     {})

