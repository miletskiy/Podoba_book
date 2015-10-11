
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse   #,reverse_lazy
# from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

from ..models.student import Student
from ..models.group import Group
# from ..models import Student, Group

from datetime import datetime

from django.views.generic import UpdateView, DeleteView, CreateView

from django.forms import ModelForm
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from django.contrib import messages
from django.contrib.messages import get_messages

from ..util import paginate, get_current_group ,get_language_cookie

# from django.forms import ValidationError

# from .student_edit import StudentEdit 357

def students_list(request):
    # check if we need to show only one group of students 
    current_group = get_current_group(request)
    if current_group:
        students = Student.objects.filter(student_group=current_group)
    else:
        # otherwise show all students
        students = Student.objects.all().order_by('last_name')
        # students = []


    # try to order students list
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket','id'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # paginate students
    # paginator = Paginator(students, 3)
    # page = request.GET.get('page')
    # try:
    #     students = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     students = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver
    #     # last page of results.
    #     students = paginator.page(paginator.num_pages)


    # apply pagination, 3 students per page
    # request = get_language_cookie(request)

    context = paginate(students, 5, request, {},
        var_name='students')

    # return render(request,'students/students_list.html',
    #     {'students':students})    
    return render(request,'students/students_list.html',
        context)


def students_add(request):
    # return HttpResponse('<h1>Student Add Form</h1>')
    # if form was post:
    if request.method == "POST":
        # if button add:
        if request.POST.get('add_button') is not None:
            # check data and collect mistakes
            # TODO: validate input from user
            errors = {}
            # validate student data will go here
            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}
            # validate user input
            first_name = request.POST.get('first_name', '').strip() 
            if not first_name:
                errors['first_name'] = _(u"First Name field is required")
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip() 
            if not last_name:
                errors['last_name'] = _(u"Last Name field is required")
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip() 
            if not birthday:
                errors['birthday'] = _(u"Birthday field is required")
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = _(u"Please input correct date format. Example:1984-12-31")
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip() 
            if not ticket:
                errors['ticket'] = _(u"Ticket number is required") 
            else:
                data['ticket'] = ticket
            
            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = _(u"Please, select group for student")
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) !=1:
                    errors['student_group'] = _(u"Please, select correct group for student")
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo') 
            # validation with Django built-methods

            if photo:
                file_extensions = ['jpeg','.jpg','.png','.gif']
                name_file = str(photo.name)
                # typed = str(photo.content_type)
                if photo.multiple_chunks():
                    errors['photo'] = _(u"Too big file. Max 2.5 Mb")
                elif name_file[-4:] not in file_extensions:
                    errors['photo'] = _(u"File extension incorrect. Choose next: *.jpg, *.jpeg, *.png, *.gif")
                    # errors['photo'] = str(photo.name) 
                else:
                    data['photo'] = photo
            # if data correct:
            if not errors:
                # add student to base
                student = Student(**data)
                # student = Student(
                #                   first_name=request.POST['first_name'],
                #                   last_name=request.POST['last_name'],
                #                   middle_name=request.POST['middle_name'],
                #                   birthday=request.POST['birthday'],
                #                   ticket=request.POST['ticket'],
                #                   student_group=Group.objects.get(pk=request.POST['student_group']), 
                #                   photo=request.FILES['photo'],
                #                  )
                student.save()
                # return to students list
                messages.success(request, _(u"The student %s was successfully added.")  % Student.objects.last())
                # return HttpResponseRedirect(
                #     u'%s?status_message=The student %s was successfully added!' %
                #         (reverse('home'),Student.objects.last()))
                return HttpResponseRedirect(reverse('home'),messages)


            # if data incorrect:   
            else:
                # return form with mistakes

                messages.error(request, _(u"Please, fix the following errors: "))
                return render(request, 'students/students_add.html',
                                {'groups': Group.objects.all().order_by('title'),
                                 'errors': errors})
        # if button cancel:
        elif request.POST.get('cancel_button') is not None:
            # return to students list

            # return HttpResponseRedirect(
            #     u'%s?status_message=Add student cancelled!' %
            #     reverse('home')) 
            messages.info(request, _(u"Add student cancelled."))
            return HttpResponseRedirect(reverse('home'))
    # if form was NOT post:
    else:
        # return form 
        return render(request, 'students/students_add.html',
                        {'groups': Group.objects.all().order_by('title')})



    return render(request,'students/students_add.html',
        {'groups':Group.objects.all().order_by('title')})


def students_edit(request,sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)



def students_delete(request,sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)


        # using class for add student

class StudentAddForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self,*args, **kwargs):
        super(StudentAddForm,self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

            # return HttpResponseRedirect(
            #     u'%s?status_message=5' %  reverse('home'))


        # set form tag attributes
        self.helper.form_action = reverse('students_add')
        # self.helper.form_action = u'%s?status_message=5' % reverse('students_add')

        self.helper.form_method = 'POST'
        self.helper.form_class = 'col-sm-12 form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-8 input-group'

        # add buttons
        # self.helper.layout.fields.append(self)
        self.helper.layout.fields.append(FormActions(
            Submit('add_button', _(u'Save'), css_class="btn btn-primary"),
            Submit('cancel_button', _(u'Cancel'), css_class="btn btn-link"),
        ))


 # using class for add student

class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        # fields = ('first_name', 'last_name', 'middle_name', 'birthday','student_group', 'photo', 'ticket', 'notes')
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('students_edit',
            kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'col-sm-12 form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-8'

        # add buttons
        # self.helper.layout.fields.append(self)
        self.helper.layout.fields.append(FormActions(
            Submit('add_button', _(u'Save'), css_class="btn btn-primary"),
            Submit('cancel_button', _(u'Cancel'), css_class="btn btn-link"),
        ))
        # self.helper.layout[-1] = FormActions(
        #     Submit('add_button', u'Save', css_class="btn btn-primary"),
        #     Submit('cancel_button', u'Cancel', css_class="btn btn-link"),
        # )


class StudentAddView(CreateView):
    model = Student
    # fields = '__all__'
    template_name = 'students/students_edit.html'
    form_class = StudentAddForm

    def get_success_url(self):
        return reverse('home')

    def post(self, request, *args, **kwargs):

        if request.POST.get('cancel_button'):

            messages.error(request, _(u"Add student cancelled.") )

            return HttpResponseRedirect(reverse('home'))

        else:
            fn=request.POST['first_name']
            ln=request.POST['last_name']
            # if StudentAddView().form_valid(form):
            # TODO: add validation fields --- form_valid
            if fn and ln:
                storage = get_messages(request) #removing all messages thanks Ivan Savchenko
                for message in storage:
                    pass
                messages.success(request, _(u"The student %(fname)s %(lname)s was successfully added.") % {'fname':fn,'lname':ln})

            return super(StudentAddView, self).post(request, *args, **kwargs)


class StudentUpdateView(UpdateView):
    # class Meta:
    #     """docstring for Meta"""
    #     model = Student

    # fields = '__all__'
    model = Student
    template_name = 'students/students_edit.html'
    # fields = {'first_name', 'last_name', 'middle_name', 'student_group', 'birthday', 'photo', 'ticket', 'notes'}
    form_class = StudentUpdateForm
    # form_class = StudentEdit

    def get_success_url(self):
        return reverse('home')

    def post(self, request, *args, **kwargs):
        stud = self.get_object()
        # group = Group.objects.filter(starosta=stud)
        # number = group.id
        # stgr = stud.student_group
        # errors = {}
        # pk= stud.id

        if request.POST.get('cancel_button'):
 
            # stud = self.get_object()
            messages.success(request, _(u"Edit student %(st)s cancelled.") % {'st':stud} )


            
            return HttpResponseRedirect(reverse('home'),messages)

        else:

            # TODO:add validation fields  ---form_valid
            if request.POST['first_name'] and request.POST['last_name']:
                storage = get_messages(request) #removing all messages thanks Ivan Savchenko
                for message in storage:
                    pass
                messages.success(request, _(u"Student info %s successfully updated.") % stud )

            return super(StudentUpdateView, self).post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return reverse('home')


    def post(self, request, *args, **kwargs):
        stud = self.get_object()
        messages.success(request, _(u"Student %s successfully deleted.") % stud)

        return super(StudentDeleteView,self).post(request,*args,**kwargs)


def students_delete_my(request, pk):
    """ Delete student by hands """
    
    student = Student.objects.get(pk = pk)
    fn = student.first_name
    ln = student.last_name

    if request.method == 'POST':
        if request.POST.get('delete_button') is not None:
            student.delete()
            messages.success(request, _(u"Student %(fname)s %(lname)s successfully deleted.") % {'fname':fn,'lname':ln})

            return HttpResponseRedirect(reverse('home'))

        elif request.POST.get('cancel_button') is not None:
            messages.error(request, _(u"Delete student %(fname)s %(lname)s cancelled.") % {'fname':fn,'lname':ln})
            return HttpResponseRedirect(reverse('home'))

    else:
        return render(request,'confirm_delete/students_ruki_confirm_delete.html',
                          {'student':student})

