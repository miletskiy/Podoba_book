# -*- coding: utf-8 -*-

from django.shortcuts import render
# from django.http import HttpResponse ,HttpRequest
# from django.template import RequestContext, loader

from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

from ..models.exam import Exam

from ..util import  get_current_group 

from django.forms import ModelForm

from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from django.views.generic import CreateView, UpdateView, DeleteView

from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from ..models.group import Group

# Views for Exams
def exams_list(request):
   # check if we need to show only one group of students 
    current_group = get_current_group(request)
    if current_group:
        exams = Exam.objects.filter(exam_group=current_group)
        # exams=[current_group]
    else:
        # otherwise show all students
        exams = Exam.objects.all().order_by('nazva')
        # students = Student.objects.all().order_by('last_name')


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

    

# Add exams form
class ExamAddForm(ModelForm):
    """docstring for ExamAddForm"""
    class Meta:
        model = Exam
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ExamAddForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper(self)

        self.helper.form_action = reverse('exams_add')

        self.helper.form_method = 'POST'
        self.helper.form_class = 'col-sm-12 form-horizontal'

        # field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-8'

        # buttons
        self.helper.layout.fields.append(FormActions(
            Submit('add_button', u'Додати', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
        ))

# Edit exams form
class ExamEditForm(ModelForm):
    """docstring for ExamEditForm"""
    class Meta:
        model = Exam
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ExamEditForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_action = reverse('exams_edit',
            kwargs={'pk': kwargs['instance'].id})

        self.helper.form_method = 'POST'
        self.helper.form_class = 'col-sm-12 form-horizontal'

        # field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-8'

        # buttons
        self.helper.layout.fields.append(FormActions(
            Submit('edit_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
        ))
# Base view for Exams
class BaseExamFormView(object):
    """docstring for BaseExamFormView"""

    def get_success_url(self):
        return reverse('exams')

# Add exam views
class ExamAddView(BaseExamFormView, CreateView):
    """docstring for ExamAddView"""
    model = Exam
    template_name = 'students/exams_add_edit.html'
    form_class = ExamAddForm

    def post(self, request, *args, **kwargs):

        if request.POST.get('cancel_button'):
            messages.error(request, u'Додавання іспиту messages відмінено! !' )
            return HttpResponseRedirect(reverse('exams'))
        else:
            nazva = request.POST['nazva']
            group = request.POST['exam_group']
            storage = get_messages(request) #removing all messages thanks Ivan Savchenko. Do not work ((
            for message in storage:
                pass
            messages.success(request, u'Iспит %s для %s успішно messages додано' % (nazva,group) )

            return super(ExamAddView, self).post(request, *args, **kwargs)


# Edit exam views
class ExamEditView(BaseExamFormView, UpdateView):
    """docstring for ExamEditView"""
    model = Exam
    template_name = 'students/exams_add_edit.html'
    form_class = ExamEditForm
 
    def post(self, request, *args, **kwargs):
        exam = self.get_object()

        if request.POST.get('cancel_button'):
            storage = get_messages(request) #removing all messages thanks Ivan Savchenko
            for message in storage:
                pass
            messages.error(request, u'Редагування іспиту %s відмінено' % exam.nazva )
            return HttpResponseRedirect(reverse('exams'))
        else:
            nazva = request.POST['nazva']
            # group = request.POST['exam_group']
            # pk = group
            storage = get_messages(request) #removing all messages thanks Ivan Savchenko
            for message in storage:
                pass
            # wsx = pk.decode('utf-8')
            # qw=Group.objects.filter(pk=wsx)
            messages.success(request, u'Iспит %s успішно змінено.' % nazva )

            return super(ExamEditView, self).post(request, *args, **kwargs)


class ExamDeleteView(BaseExamFormView, DeleteView):
    """docstring for ExamDeleteView"""
    model = Exam
    template_name = 'students/exams_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        exam = self.get_object()
        messages.success(request, u'Iспит %s успішно messages видалено!! messages!'% exam )

        return super(ExamDeleteView,self).post(request,*args,**kwargs)




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
