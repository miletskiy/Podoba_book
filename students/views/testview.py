# -*- coding: utf-8 -*-

from django.views.generic import ListView
# from models.student import Student
from ..models.student import Student

class StudentList(ListView):
    model = Student
    template_name = "temp5.html"
    context_object_name = 'students'

    def get_context_data(self, **kwargs):

        """This method adds extra variables to template"""

        context = super(StudentList, self).get_context_data(**kwargs)
        context['show_logo'] = False
        return context
        # get original context data from parent class

        # tell template not to show logo on a page

        # return context mapping
        # return context

    def get_queryset(self):
        """Order students by last_name."""
        # get original query set
        qs = super(StudentList, self).get_queryset()
        # order by last name
        return qs.order_by('last_name')
