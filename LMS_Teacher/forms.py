from bootstrap3_datetime.widgets import DateTimePicker
from django.utils.translation import ugettext_lazy as _
from django import forms

from LMS.models import Assignment, Unit, GradeRecord


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'due_time', 'description']

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['due_time'].widget = DateTimePicker(options={"format": "YYYY-MM-DD HH:mm"})


class GradeEditForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['mark_assignment', 'mark_quiz', 'mark_presentation', 'mark_mid_exam', 'mark_final_exam']
        labels = {
            'mark_assignment': _('Assignment Mark'),
            'mark_quiz': _('Quiz Mark'),
            'mark_presentation': _('Presentation Mark'),
            'mark_mid_exam': _('Mid Exam Mark'),
            'mark_final_exam': _('Final Exam Mark')
        }


class GradeRecordForm(forms.ModelForm):
    class Meta:
        model = GradeRecord
        fields = ['mark_assignment', 'mark_quiz', 'mark_presentation', 'mark_mid_exam', 'mark_final_exam']
        labels = {
            'mark_assignment': _('Assignment Mark'),
            'mark_quiz': _('Quiz Mark'),
            'mark_presentation': _('Presentation Mark'),
            'mark_mid_exam': _('Mid Exam Mark'),
            'mark_final_exam': _('Final Exam Mark')
        }

    def clean(self):
        unit = self.instance.unit

        for attr in self.Meta.fields:
            _max = getattr(unit, attr)
            curr = self.cleaned_data[attr]

            if curr > _max:
                self.add_error(attr, _('Ensure this value is less than or equal to %s.') % _max)

        return self.cleaned_data
