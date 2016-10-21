from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.utils.translation import ugettext_lazy as _

from LMS.models import GENDERS, Course, TITLES, Faculty, Class


class DateInput(forms.DateInput):
    input_type = 'date'


class StudentEditForm(forms.Form):
    first_name = forms.CharField(max_length=30, min_length=2, label=_('First Name'), strip=True)
    last_name = forms.CharField(max_length=30, min_length=2, label=_('Last Name'), strip=True)
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDERS, label=_('Gender'))
    year = forms.IntegerField(label=_('Year'))
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label=_('Course'))
    start_date = forms.DateField(label=_('Start Date'), widget=DateInput())
    email = forms.EmailField(label=_('Email'))
    password = forms.CharField(label=_('Password'))


class TeacherEditForm(forms.Form):
    title = forms.ChoiceField(choices=TITLES, label=_('Title'))
    first_name = forms.CharField(max_length=30, min_length=2, label=_('First Name'), strip=True)
    last_name = forms.CharField(max_length=30, min_length=2, label=_('Last Name'), strip=True)
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDERS, label=_('Gender'))
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), label=_('Faculty'))
    password = forms.CharField(label=_('Password'))


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['day', 'start_time', 'end_time', 'start_week', 'end_week', 'type', 'location']

    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].widget = DateTimePicker(options={"format": "HH:mm"},
                                                          icon_attrs={'class': 'glyphicon glyphicon-time'})
        self.fields['end_time'].widget = DateTimePicker(options={"format": "HH:mm"},
                                                        icon_attrs={'class': 'glyphicon glyphicon-time'})

    def clean(self):
        cleaned_data = super(ClassForm, self).clean()

        error = {}
        if 'start_time' in cleaned_data and 'end_time' in cleaned_data:
            if cleaned_data['start_time'] >= cleaned_data['end_time']:
                error.update({'end_time': _("End time must larger than start time.")})

        if 'start_week' in cleaned_data and 'end_week' in cleaned_data:
            if cleaned_data['start_week'] > cleaned_data['end_week']:
                error.update({'end_week': _("End week must not smaller than start week.")})
            elif cleaned_data['start_week'] <= 0:
                error.update({'start_week': _("Must larger than 0.")})

        if error:
            raise forms.ValidationError(error)

        return cleaned_data
