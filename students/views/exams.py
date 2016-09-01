
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext as _

from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from ..models.exam import Exam
from ..util import get_current_group, paginate
from ..models.group import Group

# Views for Exams


def exams_list(request):
   # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        exams = Exam.objects.filter(exam_group=current_group)
    else:
        # otherwise show all students
        exams = Exam.objects.all().order_by('nazva')

    context = paginate(exams, 2, request, {},
                       var_name='exams')

    return render(request, 'students/exams_list.html',
                  context)


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
            Submit('add_button', _(u'Save'), css_class="btn btn-primary"),
            Submit('cancel_button', _(u'Cancel'), css_class="btn btn-link"),
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
            Submit('edit_button', _(u'Save'), css_class="btn btn-primary"),
            Submit('cancel_button', _(u'Cancel'), css_class="btn btn-link"),
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
            messages.error(request, _(u"Add exam cancelled."))
            return HttpResponseRedirect(reverse('exams'))
        else:
            nazva = request.POST['nazva']
            group = request.POST['exam_group']
            # removing all messages thanks Ivan Savchenko. Do not work ((
            storage = get_messages(request)
            for message in storage:
                pass
            messages.success(
                request, _(u"Exam %(exm)s for %(grp)s was "
                                        "successfully added ") % {
                                        'grp': group, 'exm': nazva})

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
            # removing all messages thanks Ivan Savchenko
            storage = get_messages(request)
            for message in storage:
                pass
            messages.error(request, _(u"Edit exam %(exm)s cancelled.") % {
                           'exm': exam.nazva})
            return HttpResponseRedirect(reverse('exams'))
        else:
            nazva = request.POST['nazva']
            # group = request.POST['exam_group']
            # pk = group
            # removing all messages thanks Ivan Savchenko
            storage = get_messages(request)
            for message in storage:
                pass
            # wsx = pk.decode('utf-8')
            # qw=Group.objects.filter(pk=wsx)
            messages.success(request, _(
                u"Exam %(nzv)s successfully updated.") % {'nzv': nazva})

            return super(ExamEditView, self).post(request, *args, **kwargs)


class ExamDeleteView(BaseExamFormView, DeleteView):
    """docstring for ExamDeleteView"""
    model = Exam
    template_name = 'students/exams_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        exam = self.get_object()
        messages.success(request, _(
            u"Exam %(exm)s successfully deleted.") % {'exm': exam})

        return super(ExamDeleteView, self).post(request, *args, **kwargs)


def exams_edit(request, eid):
    return HttpResponse('<h1>Edit Exam %s</h1>' % eid)


def exams_delete(request, eid):
    return HttpResponse('<h1>Delete Exam %s</h1>' % eid)
