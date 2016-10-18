from bootstrap3_datetime.widgets import DateTimePicker
from django import forms

from LMS.models import Assignment


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'due_time', 'description']

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['due_time'].widget = DateTimePicker(options={"format": "YYYY-MM-DD HH:mm", "pickSeconds": False})
