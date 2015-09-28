# -*- coding: utf-8 -*-

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

from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from django.contrib import messages
from django.contrib.messages import get_messages

from ..util import paginate, get_current_group

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
    context = paginate(students, 5, request, {},
        var_name='students')

    # return render(request,'students/students_list.html',
    #     {'students':students})    
    return render(request,'students/students_list.html',
        context)

# Views for students
# def students_list(request):
#     students = (
#         {'id':1,
#         'first_name':u'Андрей',
#         'last_name':u'Корост',
#         'ticket':235,
#         'image': 'img/me.jpeg'},
#         {'id':2,
#         'first_name':u'Светлана',
#         'last_name':u'Ильдирова',
#         'ticket':2358,
#         'image': 'img/piv.png'},
#         {'id':3,
#         'first_name':u'Василий',
#         'last_name':u'Пупкин',
#         'ticket':2935,
#         'image': 'img/podoba3.jpg'},
#     )
#     return render(request, 'students/students_list.html',
#         {'students': students})


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
                errors['first_name'] = u"Ім'я є обов'язковим" 
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip() 
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим" 
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip() 
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язково"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u'Введіть коректний формат дати (напр. 1984-12-31)'
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip() 
            if not ticket:
                errors['ticket'] = u"Номер білета є обов'язковим" 
            else:
                data['ticket'] = ticket
            
            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) !=1:
                    errors['student_group'] = u"Оберіть коректну групу для студента"
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo') 
            # validation with Django built-methods

            if photo:
                file_extensions = ['jpeg','.jpg','.png','.gif']
                name_file = str(photo.name)
                # typed = str(photo.content_type)
                if photo.multiple_chunks():
                    errors['photo'] = u"Занадто великий файл. Максимум 2.5 Mb"
                elif name_file[-4:] not in file_extensions:
                    errors['photo'] = u"Невірний формат файлу. Оберіть зображення *.jpg, *.jpeg, *.png, *.gif" 
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
                messages.success(request, u'Студента %s успішно додано за допомогою messages!' % Student.objects.last())
                # return HttpResponseRedirect(
                #     u'%s?status_message=Студента %s успішно додано!' %
                #         (reverse('home'),Student.objects.last()))
                return HttpResponseRedirect(reverse('home'),messages)


            # if data incorrect:
            else:
                # return form with mistakes

                messages.error(request, u'Будь-ласка, виправте наступні помилки: messages')
                return render(request, 'students/students_add.html',
                                {'groups': Group.objects.all().order_by('title'),
                                 'errors': errors})
        # if button cancel:
        elif request.POST.get('cancel_button') is not None:
            # return to students list

            # return HttpResponseRedirect(
            #     u'%s?status_message=Додавання студента скасовано!' %
            #     reverse('home'))
            messages.info(request, u'Додавання студента скасовано! messages!')
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
        self.helper.field_class = 'col-sm-8'

        # add buttons
        # self.helper.layout.fields.append(self)
        self.helper.layout.fields.append(FormActions(
            Submit('add_button', u'Додати', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
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
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
        ))
        # self.helper.layout[-1] = FormActions(
        #     Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
        #     Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
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

            messages.error(request, u'Додавання студента messag відмінено! es!' )

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
                messages.success(request, u'Студента %s %s успішно messages збережено  ! !' % (fn, ln) )

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
        # return u'%s?status_message=Студента успішно збережено!' \
        #     % reverse('home')
        # messages.success(request, u'Студента успішно збережено! messages!')
        # storage = get_messages(request)
        # messages.add_message(request, messages.INFO, 'Hello world.')
        # return HttpResponseRedirect(reverse('home'),messages)

        # return u'%s?status_message=Студента успішно збережено!' \
        #     % reverse('home')

    def post(self, request, *args, **kwargs):
        stud = self.get_object()
        # group = Group.objects.filter(starosta=stud)
        # number = group.id
        # stgr = stud.student_group
        # errors = {}
        # pk= stud.id

        if request.POST.get('cancel_button'):
            # return HttpResponseRedirect(
            #     u'%s?status_message=Редагування студента відмінено!' %
            #     reverse('home'))
            # messages.success(request, u'Редагування студента відмінено! messages!')
            # stud = self.get_object()
            messages.success(request, u'Редагування студента %s відмінено! messages!' % stud )

            return HttpResponseRedirect(reverse('home'),messages)

        else:

            # if len(group) > 0 and stud.student_group !=  group :
            #     # raise ValidationError(u'Студент є старостою іншої групи.',
            #     #     code='invalid')
            #     errors['student_group']= u'Студент є старостою іншої групи.'
            #
            #     storage = get_messages(request) #removing all messages thanks Ivan Savchenko
            #     for message in storage:
            #         pass
            #     messages.success(request, u'Студент %s є старостою іншої групи.  message ' % stud)
            #
            #     # return HttpResponseRedirect(reverse('groups'),messages)
            #     return HttpResponseRedirect(reverse('students_edit',kwargs={'pk':pk}))
                # return super(StudentUpdateView, self).post(request, *args, **kwargs)
            # else:
            # TODO:add validation fields  ---form_valid
            if request.POST['first_name'] and request.POST['last_name']:
                storage = get_messages(request) #removing all messages thanks Ivan Savchenko
                for message in storage:
                    pass
                messages.success(request, u'Iнформація студента %s успішно оновлена! messages!' % stud)

            return super(StudentUpdateView, self).post(request, *args, **kwargs)







class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return reverse('home')

        # return u'%s?status_message=Студента успішно видалено!' \
        #     % reverse('home')

    def post(self, request, *args, **kwargs):
        stud = self.get_object()
        messages.success(request, u'Студента %s успішно messages видалено!! !'% stud)

        return super(StudentDeleteView,self).post(request,*args,**kwargs)


def students_delete_my(request, pk):
    """ Delete student by hands """
    
    student = Student.objects.get(pk = pk)
    fn = student.first_name
    ln = student.last_name

    if request.method == 'POST':
        if request.POST.get('delete_button') is not None:
            student.delete()
            messages.success(request, u'Студента %s %s успішно messages видалено!! !' % (fn,ln))
            return HttpResponseRedirect(reverse('home'))

        elif request.POST.get('cancel_button') is not None:
            messages.error(request, u'Видалення Студента %s %s скасовано messages!' % (fn,ln))
            return HttpResponseRedirect(reverse('home'))

    else:
        return render(request,'confirm_delete/students_ruki_confirm_delete.html',
                          {'student':student})