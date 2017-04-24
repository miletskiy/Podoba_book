# -*- coding: utf-8 -*-

from django.contrib import admin
from .models.student import Student
from .models.group import Group
from .models.exam import Exam
from .models.monthjournal import MonthJournal

# Register your models here.
# admin.site.register(Student,StudentAdmin)
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError, Form, ModelChoiceField
from django.shortcuts import render


class StudentFormAdmin(ModelForm):

    def clean_student_group(self):
        """Check if student is leader in any group.

        If yes, then ensure it's the same as selected group."""
        # get group where current student is a leader
        groups = Group.objects.filter(starosta=self.instance)
        if len(groups) > 0 and \
            self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(u'Студент є старостою іншої групи.',
                code='invalid')

        return self.cleaned_data['student_group']

# from students.models.group import Group

class UpdateGroupForm(Form):

    group = ModelChoiceField(queryset=Group.objects.all().order_by('title'), required=False)

    # class Meta:
    #     model = Group
    #     fields = "group",

class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'ticket', 'student_group','photo', 'edit']
    list_display_links = ['last_name', 'first_name', 'edit']
    # list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 7
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket',
        'notes']
    form = StudentFormAdmin
    # form = UpdateGroupForm
    actions = ['make_krasivo', 'change_group','copy_student' , "update_group"]

    def edit(self, obj):
        return 'Edit'

    def update_group(modeladmin, request, queryset):
        print request.POST
        import pdb;
        pdb.set_trace()
        form = UpdateGroupForm(request.POST)
        if 'change_group' in request.POST:
            import pdb;pdb.set_trace()
            form = UpdateGroupForm(request.POST)
            if form.is_valid():
                group = form.cleaned_data['group']
                updated_group = queryset.update(student_group=group)
                counter = queryset.count
                modeladmin.message_user(request, u"У %s студентів було змненно групу на %s") % (counter, group)
                return HttpResponseRedirect(request.get_full_path())

            else:
                form = UpdateGroupForm()
            # return (request, 'students/students_list.html.html', {'students': queryset, 'form': form, 'title': u'Зміна групи'})
        # print (request, 'students/change_group.html', {'students': queryset, 'form': form, 'title': u'Зміна групи'})
        # return HttpResponseRedirect ('/students/change_group.html',{'students':queryset,'form':form,'title':u'Зміна групи'})
        return render(request, 'students/change_group.html',{'students':queryset,'form':form,'title':u'Зміна групи'})
        # return (request, 'students/change_group.html', {'students': queryset, 'form': form, 'title': u'Зміна групи'})

    update_group.short_description = u'Перемістити у групу'




# Testoviy method for actions. domashka370

    def make_krasivo(self, request , queryset ):
        if len(queryset) == 1:
            message_bit = "For selected student"
        else:
            message_bit = "For selected students"
        self.message_user(request, "%s made good." % message_bit)

    make_krasivo.short_description = u'Сделать хорошо'

# Action deletion student from group. domashka370
    def change_group(self, request , queryset):
        queryset.update(student_group = None)
        self.message_user(request, "Group was changed. Student free for any group now.")

    change_group.short_description = u"Удалить из группы"

# Copy selected student. domashka370

    def copy_student(self, request , queryset):
        for ob in queryset:
            ob.pk = None
            ob.save()
        self.message_user(request, "Selected student was copied.")

    copy_student.short_description = u"Копировать студента"

    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk': obj.id})


# Form edit group with validation starosta field. domashka374
class GroupFormAdmin(ModelForm):

    def clean_starosta(self):
        """Check  whether the student member of  this group.

        If yes, then ensure it's the same as selected student."""

        # get students from current group:
        students = Student.objects.filter(student_group=self.instance)

        # if self.cleaned_data['starosta'] != students[0]:
        # if self.cleaned_data['starosta'] not in students:# and len(students) > 0:
        if self.cleaned_data['starosta'] in students or self.cleaned_data['starosta'] is None:# and len(students) > 0:
        # if self.cleaned_data['starosta'] in students :# and len(students) > 0:
            return self.cleaned_data['starosta']
        else:
            raise ValidationError(u'Студент не належить до обранои групи.\
                                    Оберіть когось з цієї групи.',
                code='invalid')

        # return self.cleaned_data['starosta']
        # groups = Group.objects.filter(starosta=self.instance)
        # student = Student.objects.filter(student_group=self.instance)


# Change admin view for Groups
class GroupAdmin(admin.ModelAdmin):
    """Describe mapping for Group in admin"""
    list_display = ['title', 'starosta', 'notes']
    list_display_links = ['title', 'notes']
    list_editable = ['starosta']
    ordering = ['title']
    list_filter = ['title']
    list_per_page = 5
    search_fields = ['title', 'starosta','notes']
    form = GroupFormAdmin
    # actions = ['make_krasivo', 'change_group','copy_student' ]

    def view_on_site(self, obj):
        return reverse('groups_edit', kwargs={'pk': obj.id})

# Change admin view for Groups
class ExamAdmin(admin.ModelAdmin):
    """Describe mapping for Group in admin"""
    list_display = ['exam_day', 'nazva', 'prepod', 'exam_group']
    list_display_links = ['exam_day', 'prepod']
    list_editable = []
    ordering = ['exam_day']
    list_filter = ['prepod']
    list_per_page = 7
    search_fields = ['nazva', 'prepod','notes']
    # form = GroupFormAdmin
    # actions = ['make_krasivo', 'change_group','copy_student' ]

    def view_on_site(self, obj):
        return reverse('exams_edit', kwargs={'pk': obj.id})


admin.site.register(Student,StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam,ExamAdmin)
admin.site.register(MonthJournal)
