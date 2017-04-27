# studentsdb
# students/forms.py

from django.forms import (
    Form,
    ModelChoiceField,
)

from students.models.group import Group


class ChangeGroupForm(Form):
    """
    Form for admin action 'change group'
    """

    group = ModelChoiceField(queryset=Group.objects.all().order_by('title'),
                             required=False)
