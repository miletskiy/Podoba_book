
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.group import Group
from ..models.student import Student

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.messages import get_messages

from ..util import get_current_group, paginate

from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext as _


# Views for Groups
def groups_list(request):
    # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        groups = Group.objects.filter(id=current_group.id)
    else:
        # otherwise show all gpoups
        groups = Group.objects.all().order_by('title')

    # Order groups list
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'title', 'starosta'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    context = paginate(groups, 4, request, {},
                       var_name='groups')

    return render(request, 'students/groups_list.html', context)


def groups_add(request):

    # if form was post:
    if request.method == 'POST':
        #       elif Add button was press:
        if request.POST.get('add_button') is not None:
            #           validate data
            # TODO: validate input
            errors = {}
            data = {'notes': request.POST.get('notes')}

            title = request.POST.get('title')
            if not title:
                errors['title'] = _(u"Group title field is required")
            else:
                data['title'] = title

            if not errors:
                starosta = request.POST.get('starosta')
                if not starosta:
                    group = Group(
                        title=request.POST['title'],
                        notes=request.POST['notes']
                    )
                    group.save()
                else:
                    group = Group(
                        title=request.POST['title'],
                        starosta=Student.objects.get(
                            pk=request.POST['starosta']),
                        notes=request.POST['notes']
                    )
                    group.save()
                messages.success(request, _(
                    u"The group %s was successfully added.") % Group.objects.last())

                return HttpResponseRedirect(reverse('groups'))
            else:
                messages.error(request, _(
                    u"Please, fix the following errors: "))
                return render(request, 'students/groups_add.html',
                              {'students': Student.objects.all().order_by('last_name'),
                               'errors': errors})
    #       if cancel_button press:
        elif request.POST.get('cancel_button') is not None:
            #                   return group list
            messages.error(request, _(u"Add group cancelled."))
            return HttpResponseRedirect(reverse('groups'))

    # elif form was not post:
    else:

        return render(request, 'students/groups_add.html',
                      {'students': Student.objects.all().order_by('last_name')})


# Group add form for generic views
class GroupAddForm(ModelForm):
    """docstring for GroupAddForm"""
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GroupAddForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_action = reverse('groups_add')

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


# Group edit form for generic views
class GroupEditForm(ModelForm):

    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GroupEditForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_action = reverse('groups_edit',
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


# Base view for Group
class BaseGroupFormView(object):
    """docstring for BaseGroupFormView"""

    def get_success_url(self):
        return reverse('groups')


# View for group add
class GroupAddView(BaseGroupFormView, CreateView):
    """docstring for GroupAddView"""
    model = Group
    template_name = 'students/groups_add_edit.html'
    form_class = GroupAddForm

    def post(self, request, *args, **kwargs):

        if request.POST.get('cancel_button'):
            messages.error(request, _(u"Add group cancelled."))
            return HttpResponseRedirect(reverse('groups'))
        else:
            group = request.POST['title']
            # removing all messages thanks Ivan Savchenko. Do not work ((
            storage = get_messages(request)
            for message in storage:
                pass
            messages.success(request, _(
                u"The group %(grp)s  was successfully added ") % {'grp': group})

            return super(GroupAddView, self).post(request, *args, **kwargs)


# View for group edit
class GroupEditView(BaseGroupFormView, UpdateView):
    """docstring for GroupEditView"""
    model = Group
    template_name = 'students/groups_add_edit.html'
    form_class = GroupEditForm

    def post(self, request, *args, **kwargs):
        group = self.get_object()

        if request.POST.get('cancel_button'):
            # removing all messages thanks Ivan Savchenko
            storage = get_messages(request)
            for message in storage:
                pass
            messages.error(request, _(u"Edit group %(grp)s cancelled.") % {
                           'grp': group.title})
            return HttpResponseRedirect(reverse('groups'))
        else:
            title = request.POST['title']
            # group = request.POST['exam_group']
            # pk = group
            # removing all messages thanks Ivan Savchenko
            storage = get_messages(request)
            for message in storage:
                pass
            # wsx = pk.decode('utf-8')
            # qw=Group.objects.filter(pk=wsx)
            messages.success(request, _(
                u"Group %(ttl)s successfully updated.") % {'ttl': title})

            return super(GroupEditView, self).post(request, *args, **kwargs)


def groups_edit(request, pk):
    return HttpResponse('<h1>Edit Group %s</h1>' % pk)


def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)


# Delete group with django generic views
class GroupDeleteView(BaseGroupFormView, DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        group = self.get_object()
        messages.success(request, _(
            u"Group %(grp)s successfully deleted.") % {'grp': group})

        return super(GroupDeleteView, self).post(request, *args, **kwargs)


# Delete group WITHOUT django generic views
class GroupDelete(object):
    model = Group


def groups_delete_my(request, pk):
    group = Group.objects.get(pk=pk)
    title = group.title
    if request.method == 'POST':
        if request.POST.get('delete_button') is not None:
            group.delete()
            messages.success(request, _(
                u"Group %(ttl)s successfully deleted.") % {'ttl': title})
            return HttpResponseRedirect(reverse('groups'), messages)

        elif request.POST.get('cancel_button') is not None:
            messages.error(request, _(
                u"Delete Group %(ttl)s cancelled.") % {'ttl': title})
            return HttpResponseRedirect(reverse('groups'), messages)

    else:
        return render(request, 'confirm_delete/groups_ruki_confirm_delete.html',
                      {'group': group})
